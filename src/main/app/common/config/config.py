import os.path
from os import makedirs


class ServerConfig:
    def __init__(
        self,
        host: str = "127.0.0.1",
        name: str = "Server",
        port: int = 18000,
        version: str = "0.1.0",
        app_desc: str = "Server",
        api_version: str = "/v1",
        workers: int = 1,
    ) -> None:
        """
        Initializes server configuration with default host and port.

        Args:
            host (str): The server host address. Default is '127.0.0.1'.
            name (str): The server name. Default is 'Server'.
            port (int): The server port number. Default is 18000.
            version (str): The server version. Default is '0.1.0'.
            app_desc (str): The server app_desc. Default is 'server'.
            api_version (str): The server api_version. Default is 'v1'.
            workers (int): The server worker numbers. Default is 1.
        """
        self.host = host
        self.name = name
        self.port = port
        self.version = version
        self.app_desc = app_desc
        self.api_version = api_version
        self.workers = workers

    def __repr__(self) -> str:
        """
        Returns a string representation of the server configuration.

        Returns:
            str: A string representation of the ServerConfig instance.
        """
        return f"{self.__class__.__name__}({self.__dict__})"


class DatabaseConfig:
    def __init__(
        self,
        dialog: str = "sqlite",
        db_name="df.db",
        url: str = "",
        pool_recycle: int = 20,
        echo_sql: bool = True,
    ) -> None:
        """
        Initializes database configuration with a default database model.

        Args:
            dialog (str): The model of database. Default is 'sqlite'.
            db_name (str): The name of sqlite database. Default is 'server.db'.
            url (str): The url of database. Default is 'src/main/resource/alembic/db/server.db'.
            pool_recycle (int): The pool size of database. Default is 20.
            echo_sql (bool): Whether to echo sql statements. Default is True.
        """
        self.dialog = dialog
        self.db_name = db_name
        if dialog == "sqlite" and url == "":
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_dir = os.path.join(base_dir, "..", "..", "resource", "alembic", "db")
            db_dir = os.path.abspath(db_dir)
            if not os.path.exists(db_dir):
                os, makedirs(db_dir)
            bd_path = os.path.join(db_dir, self.db_name)
            url = "sqlite+aiosqlite:///" + str(bd_path)
        self.url = url
        self.pool_recycle = pool_recycle
        self.echo_sql = echo_sql

    def __repr__(self) -> str:
        """
        Returns a string representation of the database configuration.

        Returns:
            str: A string representation of the DatabaseConfig instance.
        """
        return f"{self.__class__.__name__}({self.__dict__})"


class SecurityConfig:
    def __init__(
        self,
        enable: bool = True,
        algorithm: str = "HS256",
        secret_key: str = "43365f0e3e88863ff5080ac382d7717634a8ef72d8f2b52d436fc9847dbecc64",
        access_token_expire_minutes: int = 30,
        refresh_token_expire_days: int = 30,
        enable_swagger: bool = False,
        white_list_routes: str = "",
        backend_cors_origins: str = "",
    ) -> None:
        """
        Initializes security configuration with default values for algorithm,
        secret key, and token expiration durations.

        Args:
            enable (bool): Whether to enable security. Default is True.
            algorithm (str): The encryption algorithm used for token generation.
                             Default is 'HS256'.
            secret_key (str): The secret key used for signing the tokens.
                              Default is a predefined key.
            access_token_expire_minutes (float): The number of days until the access
                                              token expires. Default is 30 minutes.
            refresh_token_expire_days (float): The number of days until the refresh
                                               token expires. Default is 30 days.
            enable_swagger (bool): Whether to enable swagger ui. Default is False
            white_list_routes (str): White list routes which can be release. Default is ""
            backend_cors_origins (str): Backend cors origins which can access. Default is ""
        """
        self.enable = enable
        self.algorithm = algorithm
        self.secret_key = secret_key
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days
        self.enable_swagger = enable_swagger
        self.white_list_routes = white_list_routes
        self.backend_cors_origins = backend_cors_origins

    def __repr__(self) -> str:
        """
        Returns a string representation of the security configuration.

        Returns:
            str: A string representation of the SecurityConfig instance,
                 showing all configuration attributes and their current values.
        """
        return f"{self.__class__.__name__}({self.__dict__})"


class Config:
    _instance = None

    def __new__(cls, config_dict=None):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, config_dict=None):
        if self.__initialized:
            return

        self.server = ServerConfig()
        self.database = DatabaseConfig()
        self.security = SecurityConfig()

        if config_dict is not None:
            self.initialize(config_dict)

        self.__initialized = True

    def initialize(self, config_dict):
        """
        Initializes the main configuration using a dictionary as the configuration source.
        """
        if "server" in config_dict:
            self.server = ServerConfig(**config_dict["server"])

        if "database" in config_dict:
            self.database = DatabaseConfig(**config_dict["database"])

        if "security" in config_dict:
            self.security = SecurityConfig(**config_dict["security"])

    def __repr__(self) -> str:
        """
        Returns a string representation of the configuration.

        Returns:
            str: A string representation of the config instance,
                 showing all configuration attributes and their current values.
        """
        return f"{self.__class__.__name__}({self.__dict__})"