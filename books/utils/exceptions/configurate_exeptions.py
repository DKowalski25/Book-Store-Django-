class ConfigurateException(ValueError):
    """Parent exception for all errors with any program configuration."""


class EnvDependNotFound(ConfigurateException):
    """Exception with env variables when it not found."""

    def __init__(self, depend_name: str):
        err_str = f'Not found end depend: {depend_name}'
        super().__init__(err_str)
