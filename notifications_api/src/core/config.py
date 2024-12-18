import os
from logging import config as logging_config

from pydantic_settings import BaseSettings

from src.core.logger import LOGGING

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BaseConfig(BaseSettings):
    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"


class AppSettings(BaseConfig):
    log_level: str = "INFO"
    batch_size: int = 100
    project_name: str = "Notifications API"

    class Config:
        env_prefix = "app_"


class PostgresSettings(BaseConfig):
    db: str = "notifications"
    user: str = "app"
    password: str = "pass"
    host: str = "localhost"
    port: int = 5432
    echo: bool = True

    class Config:
        env_prefix = "postgres_"


class RabbitMQSettings(BaseConfig):
    host: str = "localhost"
    port: int = 5672
    username: str = "guest"
    password: str = "guest"

    class Config:
        env_prefix = "rabbitmq_"


class JaegerSettings(BaseConfig):
    host: str = "localhost"
    port: int = 6831

    class Config:
        env_prefix = "jaeger_"


postgres_settings = PostgresSettings()
rabbitmq_settings = RabbitMQSettings()
jaeger_settings = JaegerSettings()
app_settings = AppSettings()
logging_config.dictConfig(LOGGING)
