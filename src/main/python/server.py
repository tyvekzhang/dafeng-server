from argparse import Namespace

from src.main.python.io.config import Config
from src.main.python.io.config_loader import ConfigLoader


def load_config(args: Namespace) -> Config:
    env = args.env

    config_file = args.config_file
    config_loader = ConfigLoader(env, config_file)
    config = config_loader.load_config()

    return Config(config)


def run(args: Namespace):
    config: Config = load_config(args)
    print(config)
