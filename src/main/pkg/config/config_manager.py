from argparse import Namespace

from src.main.pkg.config.config import Config, ServerConfig, SecurityConfig, DatabaseConfig
from src.main.pkg.config.config_loader import ConfigLoader
from src.main.pkg.exception.exception import ConfigNotInitialisedException

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