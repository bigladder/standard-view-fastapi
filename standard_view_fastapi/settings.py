from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = ".env"


class StandardViewSettings(BaseSettings):
    secret_key: str = ""
    session_age: int = 86400
    https_only: bool = False
    cache_size: int = 1000
    logging_yaml: str = ""
    logger: str = ""
    lattice_directory: str = ""
    schema_directory: str = ""

    model_config = SettingsConfigDict(env_file=ENV_FILE)
