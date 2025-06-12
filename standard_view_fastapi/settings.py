from pydantic_settings import BaseSettings, SettingsConfigDict


class StandardViewSettings(BaseSettings):
    secret_key: str = ""
    session_age: int = 86400
    https_only: bool = False
    cache_size: int = 1000
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env")
