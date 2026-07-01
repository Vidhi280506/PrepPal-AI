from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "PrepPal AI"
    VERSION: str = "1.0.0"

    DATABASE_URL: str = "sqlite:///./preppal.db"

    GOOGLE_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()