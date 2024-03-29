import logging
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class AppSettings(BaseSettings):
    smtp_server: str = 'smtp.yandex.ru'
    smtp_port: int = 465
    smtp_username: str = 'nickitakosyanov@yandex.ru'
    smtp_password: str = 'eeqpwldczuubcnzu'
    rabbitmq_host: str = 'rabbitmq'
    queue_name: str = 'notifications'
    admin_credentials: dict = {
        'email': 'a@b.com',
        'password': '123qwe'
    }
    scheme: str = "postgresql"
    postgres_db: str = "notifications"
    postgres_user: str = "app"
    postgres_password: str = "123qwe"
    postgres_host: str = "postgres-notifications"
    postgres_port: int = 5432
    login_url: str = 'http://auth-api/api/v1/auth/login'
    user_url: str = 'http://auth-api/api/v1/users/'

    @property
    def dsn(self) -> PostgresDsn:
        return str(
            PostgresDsn.build(
                scheme=self.scheme,
                username=self.postgres_user,
                password=self.postgres_password,
                host=self.postgres_host,
                port=self.postgres_port,
                path=self.postgres_db,
            )
        )


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)


logger.addHandler(console_handler)


settings = AppSettings()
