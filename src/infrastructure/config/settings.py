from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache
import os

class Settings(BaseSettings):
    app_env: str = Field(default=os.getenv("APP_ENV", "dev"), alias="APP_ENV")
    db_url: str = Field(default=os.getenv("DB_URL", "mysql+pymysql://root:password@127.0.0.1:3306/eventia"), alias="DB_URL")
    redis_url: str | None = Field(default=os.getenv("REDIS_URL"), alias="REDIS_URL")
    cache_ttl_seconds: int = Field(default=int(os.getenv("CACHE_TTL_SECONDS", "60")), alias="CACHE_TTL_SECONDS")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore