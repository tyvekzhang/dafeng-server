import os
import sys
import argparse

# Add the project path to the system path for module imports
base_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(base_dir, "..", "..")
project_path = os.path.abspath(project_dir)
sys.path.insert(0, project_path)

from src.main.python.server import run

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Custom arguments for the server")

    parser.add_argument("-e", "--env", type=str, default='dev', help="Specify the environment for the project")
    parser.add_argument("-c", "--config_file", type=str, default=None, help="Path to a custom configuration file")

    args = parser.parse_args()

    # Run the server with the parsed arguments
    run(args)