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
    def __init__(self, dialog: str = "sqlite") -> None:
        """
        Initializes database configuration with a default database type.

        Args:
            dialog (str): The type of database. Default is 'sqlite'.
        """
        self.dialog = dialog

    def __repr__(self) -> str:
        """
        Returns a string representation of the database configuration.

        Returns:
            str: A string representation of the DatabaseConfig instance.
        """
        return f"{self.__class__.__name__}({self.__dict__})"


class Config:
    def __init__(self, config_dict) -> None:
        """
        Initializes the main configuration using a dictionary as the configuration source.

        Args:
            config_dict (dict): A dictionary containing server and database configuration.
        """
        self.server = "server"
        self.database = "database"

        if self.server in config_dict:
            """
            If the server configuration is present in the dictionary,
            initializes the ServerConfig using the provided values.
            """
            self.server = ServerConfig(**config_dict[self.server])
        else:
            """
            If the server configuration is not present,
            uses the default ServerConfig.
            """
            self.server = ServerConfig()

        if self.database in config_dict:
            """
            If the database configuration is present in the dictionary,
            initializes the DatabaseConfig using the provided values.
            """
            self.database = DatabaseConfig(**config_dict[self.database])
        else:
            """
            If the database configuration is not present,
            uses the default DatabaseConfig.
            """
            self.database = DatabaseConfig()

    def __repr__(self) -> str:
        """
        Returns a string representation of the main configuration.

        Returns:
            str: A string representation of the instance.
        """
        return f"{self.__class__.__name__}({self.__dict__})"
