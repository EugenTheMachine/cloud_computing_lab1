from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"   # default на випадок запуску поза Docker
    POSTGRES_PORT: str = "5432"

    # Налаштування Pydantic v2
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",           # <-- це головне! Ігнорувати зайві поля
        case_sensitive=False
    )

    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Налаштування FastAPI
    app_host: str = "0.0.0.0"
    app_port: int = 8080


# Створюємо екземпляр
settings = Settings()