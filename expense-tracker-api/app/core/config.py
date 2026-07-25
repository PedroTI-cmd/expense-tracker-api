from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # App
    app_name: str = "Expense Tracker API"
    api_v1_prefix: str = "/api/v1"
    environment: str = "development"

    # Database
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/expenses_db"

    # Security
    secret_key: str = "change-this-secret-key-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24h


settings = Settings()
