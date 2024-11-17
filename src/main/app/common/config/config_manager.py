import os
from argparse import Namespace

from src.main.app.common.config.config import (
    Config,
    ServerConfig,
    SecurityConfig,
    DatabaseConfig,
)
from src.main.app.common.config.config_loader import ConfigLoader
from src.main.app.common.enums.enum import ResponseCode
from src.main.app.common.exception.exception import (
    ConfigNotInitialisedException,
    SystemException,
)
from src.main.app.common.util.work_path_util import resource_dir

config: Config


def load_config(args: Namespace) -> None:
    """
    Loads the configuration based on the provided command-line arguments.

    Args:
        args (Namespace): Command-line arguments containing 'env' for the environment
                          and 'config_file' for the configuration file path.

    Returns:
        Config: A configuration object populated with the loaded settings.
    """
    global config
    env = args.env

    config_file = args.config_file
    config_loader = ConfigLoader(env, config_file)
    config_dict = config_loader.load_config()
    config = Config(config_dict)


def get_database_url(*, env: str = "dev"):
    assert env in ("dev", "prod", "local")
    config_path = os.path.join(resource_dir, f"config-{env}.yml")
    config_dict = ConfigLoader.load_yaml_file(config_path)
    if "database" not in config_dict:
        raise SystemException(
            ResponseCode.PARAMETER_ERROR.code,
            f"{ResponseCode.PARAMETER_ERROR.msg}: {env}",
        )
    return config_dict["database"]["url"]


def get_config() -> Config:
    """
    Return config content
    """
    if not config:
        raise ConfigNotInitialisedException
    return config


def get_server_config() -> ServerConfig:
    """
    Return server config content
    """
    return config.server


def get_security_config() -> SecurityConfig:
    """
    Return security config content
    """
    return config.security


def get_database_config() -> DatabaseConfig:
    """
    Return database config content
    """
    return config.database
