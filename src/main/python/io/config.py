class ServerConfig:
    def __init__(self, host: str = '127.0.0.1', port: int = 18000) -> None:
        """
        Initializes server configuration with default host and port.

        Args:
            host (str): The server host address. Default is '127.0.0.1'.
            port (int): The server port number. Default is 18000.
        """
        self.host = host  # Server host address
        self.port = port  # Server port number

    def __repr__(self) -> str:
        """
        Returns a string representation of the server configuration.

        Returns:
            str: A string representation of the ServerConfig instance.
        """
        return f"{self.__class__.__name__}({self.__dict__})"


class DatabaseConfig:
    def __init__(self, dialog: str = 'sqlite') -> None:
        """
        Initializes database configuration with a default database type.

        Args:
            dialog (str): The type of database. Default is 'sqlite'.
        """
        self.dialog = dialog  # Type of database

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
        self.server = "server"  # Key for server configuration
        self.database = "database"  # Key for database configuration

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
            str: A string representation of the Config instance.
        """
        return f"{self.__class__.__name__}({self.__dict__})"