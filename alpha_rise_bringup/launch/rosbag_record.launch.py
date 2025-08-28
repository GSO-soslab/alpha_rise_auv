from launch import LaunchDescription
from launch.actions import ExecuteProcess, RegisterEventHandler, OpaqueFunction
from launch.event_handlers import OnProcessExit
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


def find_latest_rosbag_dir(output_dir: Path):
    print(f"[INFO] Searching for rosbag2 directories in: {output_dir}")
    bag_dirs = [p for p in output_dir.iterdir() if p.is_dir() and p.name.startswith("rosbag2_")]
    if not bag_dirs:
        raise FileNotFoundError("No rosbag2 directory found.")
    return max(bag_dirs, key=lambda p: p.stat().st_mtime)


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

        bag_dir = find_latest_rosbag_dir(BAG_OUTPUT_DIR)
        print(f"[INFO] Found bag directory: {bag_dir}")
        merge_yaml_files(config_paths, bag_dir)

    except Exception as e:
        print(f"[ERROR] Post-processing failed: {e}")

    return []


def generate_launch_description():
     # Ensure the output directory exists before recording
    BAG_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    rosbag_record = ExecuteProcess(
        cmd=["ros2", "bag", "record", "-a"],
        cwd=str(BAG_OUTPUT_DIR),
        output="screen"
    )

    on_rosbag_exit = RegisterEventHandler(
        OnProcessExit(
            target_action=rosbag_record,
            on_exit=[OpaqueFunction(function=post_process)]
        )
    )

    return LaunchDescription([
        rosbag_record,
        on_rosbag_exit
    ])
