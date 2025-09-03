from launch import LaunchDescription
from launch.actions import ExecuteProcess, RegisterEventHandler, OpaqueFunction
from launch.event_handlers import OnProcessStart
import os
import yaml
from pathlib import Path
import datetime

# ───────────── LOAD CONFIG FROM YAML ───────────── #
CONFIG_PATH = Path(__file__).parent.parent / "config" / "rosbag_record.yaml"

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

WORKSPACE_NAME = config["workspace_name"]
PACKAGE_NAMES = config["package_names"]

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
            yaml_files.extend(config_root.rglob("*.yaml"))

    if not yaml_files:
        print("[ERROR] No YAML files found.")
        return

    master_data = {}
    for yfile in yaml_files:
        try:
            with open(yfile, "r") as f:
                data = yaml.safe_load(f)
                if isinstance(data, dict):
                    master_data.update(data)
                else:
                    print(f"[WARNING] Skipping non-dictionary file: {yfile}")
        except yaml.YAMLError as e:
            print(f"[ERROR] Failed to parse {yfile}: {e}")

    output_file = output_path / "params.yaml"
    with open(output_file, "w") as f:
        yaml.dump(master_data, f)
    print(f"[INFO] Merged YAML written to: {output_file}")


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

    except Exception as e:
        print(f"[ERROR] Post-processing failed: {e}")

    return []


# ───────────── MAIN LAUNCH DESCRIPTION ───────────── #
def generate_launch_description():
    # Create session directory before anything runs
    SESSION_DIR.mkdir(parents=True, exist_ok=True)

    # Start rosbag recording in the session directory (rosbag2_0 will be created by ros2)
    rosbag_record = ExecuteProcess(
        cmd=["ros2", "bag", "record", "-a"],
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
