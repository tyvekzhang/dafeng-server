import os
import sys
import argparse

from src.main.app.common.config.config_manager import load_config

# Add the project path to the system path for module imports
base_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(base_dir, os.pardir, os.pardir)
project_path = os.path.abspath(project_dir)
sys.path.insert(0, project_path)


# Run the server
def run():
    from src.main.app import server

    server.run()


# Load the configuration and run the server
def main():
    parser = argparse.ArgumentParser(description="Custom arguments for the server")

    parser.add_argument(
        "-e",
        "--env",
        type=str,
        default="dev",
        help="Specify the environment for the project",
    )
    parser.add_argument(
        "-c",
        "--config_file",
        type=str,
        default=None,
        help="Path to a custom configuration file",
    )

    args = parser.parse_args()

    load_config(args)
    run()


if __name__ == "__main__":
    main()
