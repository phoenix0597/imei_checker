from os.path import abspath, dirname, join

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # Telegram
    BOT_TOKEN: str

    # API
    # API_TOKEN: str
    IMEI_CHECK_API_KEY_SANDBOX: str
    IMEI_CHECK_API_KEY_LIVE: str
    IMEI_CHECK_API_URL: str = "https://api.imeicheck.net/v1"

    # Security
    # API_TOKEN_EXPIRE_MINUTES: int = 30
    # SECRET_KEY: str

    BASE_DIR: str = abspath(dirname(dirname(dirname(__file__))))
    ENV_FILE_PATH: str = join(BASE_DIR, ".env")

    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, extra="ignore")


settings = Settings()  # type: ignore
