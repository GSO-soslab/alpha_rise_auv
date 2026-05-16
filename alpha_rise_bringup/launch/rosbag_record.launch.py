from launch import LaunchDescription
from launch.actions import ExecuteProcess, RegisterEventHandler, OpaqueFunction
from launch.event_handlers import OnProcessStart
import os
import shutil
import yaml
from pathlib import Path
import datetime

# ───────────── LOAD CONFIG FROM YAML ───────────── #
CONFIG_PATH = Path(__file__).parent.parent / "config" / "rosbag_record.yaml"

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

WORKSPACE_NAME = config["workspace_name"]
PACKAGE_NAMES = config["package_names"]
URDF_PACKAGE_NAMES = config["urdf_package_names"]

USER_NAME = os.getenv("USER") or os.getlogin()
INSTALL_BASE = Path(f"/home/{USER_NAME}/{WORKSPACE_NAME}/install")

# Expand user (~ or $HOME) in output path
BAG_OUTPUT_DIR = Path(os.path.expanduser(config["bag_output_dir"]))

# ───────────── CREATE SESSION DIRECTORY ───────────── #
TIMESTAMP = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
SESSION_DIR = BAG_OUTPUT_DIR / f"rosbag2_{TIMESTAMP}"
ROSBAG_DIR = SESSION_DIR / "rosbag2_"


# ───────────── HELPER FUNCTIONS ───────────── #
def find_all_config_dirs(package_path: Path):
    return [p for p in package_path.iterdir() if p.is_dir() and p.name.endswith("config")]


def merge_yaml_files(config_paths: list[Path], output_path: Path):
    yaml_files = []
    for config_root in config_paths:
        if config_root.exists():
            yaml_files.extend([
                yfile for yfile in config_root.rglob("*.yaml")
            ])

    if not yaml_files:
        print("[ERROR] No YAML files found (excluding *_sim.yaml).")
        return

    master_data = {}
    for yfile in yaml_files:
        try:
            with open(yfile, "r") as f:
                data = yaml.safe_load(f)
                if isinstance(data, dict):
                    key_name = yfile.name  # or yfile.stem if you want to strip ".yaml"
                    master_data[key_name] = data
                else:
                    print(f"[WARNING] Skipping non-dictionary file: {yfile}")
        except yaml.YAMLError as e:
            print(f"[ERROR] Failed to parse {yfile}: {e}")

    output_file = output_path / "params.yaml"
    with open(output_file, "w") as f:
        yaml.dump(master_data, f, default_flow_style=False)

    print(f"[INFO] Merged YAML written to: {output_file}")

def copy_urdf_files(package_paths: list[Path], output_path: Path):
    for pkg_path in package_paths:
        urdf_files = list(pkg_path.rglob("*.urdf"))
        if not urdf_files:
            print(f"[WARNING] No .urdf files found in: {pkg_path}")
            continue
        for urdf_file in urdf_files:
            dest = output_path / urdf_file.name
            shutil.copy2(urdf_file, dest)
            print(f"[INFO] Copied URDF: {urdf_file} -> {dest}")


def post_process(context, *args, **kwargs):
    try:
        package_paths = [
            INSTALL_BASE / pkg / "share" / pkg for pkg in PACKAGE_NAMES
        ]
        config_paths = [
            config_dir
            for pkg_path in package_paths
            for config_dir in find_all_config_dirs(pkg_path)
        ]

        if not config_paths:
            print("[ERROR] No config directories found.")
            return []

        print(f"[INFO] Writing merged config into: {SESSION_DIR}")
        merge_yaml_files(config_paths, SESSION_DIR)

        urdf_package_paths = [
            INSTALL_BASE / pkg / "share" / pkg for pkg in URDF_PACKAGE_NAMES
        ]
        copy_urdf_files(urdf_package_paths, SESSION_DIR)

    except Exception as e:
        print(f"[ERROR] Post-processing failed: {e}")

    return []


# ───────────── QOS OVERRIDES ───────────── #
QOS_OVERRIDES = {
    "/tf_static": {
        "reliability": "reliable",
        "durability": "transient_local",
        "history": "keep_last",
        "depth": 1,
    }
}


# ───────────── MAIN LAUNCH DESCRIPTION ───────────── #
def generate_launch_description():
    # Create session directory before anything runs
    SESSION_DIR.mkdir(parents=True, exist_ok=True)

    # Write QoS overrides so /tf_static is recorded with transient_local durability
    qos_file = SESSION_DIR / "qos_overrides.yaml"
    with open(qos_file, "w") as f:
        yaml.dump(QOS_OVERRIDES, f)

    # Start rosbag recording in the session directory (rosbag2_0 will be created by ros2)
    rosbag_record = ExecuteProcess(
        cmd=["ros2", "bag", "record", "-a",
             "--qos-profile-overrides-path", str(qos_file)],
        cwd=str(SESSION_DIR),
        output="screen"
    )

    # Run post-processing (yaml merge) as soon as rosbag starts
    on_rosbag_start_handler = RegisterEventHandler(
        OnProcessStart(
            target_action=rosbag_record,
            on_start=[
                OpaqueFunction(function=post_process)
            ]
        )
    )

    return LaunchDescription([
        rosbag_record,
        on_rosbag_start_handler
    ])
