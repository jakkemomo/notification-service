import pathlib
from os import environ as env

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()

BASE_DIR = pathlib.Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = BASE_DIR / "config" / "communication_api.json"


class RabbitSettings(BaseSettings):
    scheme: str = Field("amqp")
    host: str = Field("localhost", env="RABBIT_HOST")
    port: int = Field(5672, env="RABBIT_PORT")
    exchange: str = env.get("EXCHANGE_NAME", "notifications")

    def get_uri(self):
        return f"{self.scheme}://{self.host}:{self.port}/"


class MongoSettings(BaseSettings):
    scheme: str = Field("mongodb")
    host: str = Field("localhost", env="MONGO_HOST")
    port: int = Field(27017, env="MONGO_PORT")
    db: str = Field("default", env="MONGO_DB")

    def get_uri(self):
        return f"{self.scheme}://{self.host}:{self.port}/"


class NotificationAppSettings(BaseSettings):
    scheme: str = Field("http")
    host: str = Field("localhost", env="NOTIFICATION_APP_HOST")
    port: int = Field(8000, env="NOTIFICATION_APP_PORT")
    service_path: str = Field("service/user/{user_id}/notice")

    def get_uri(self):
        return f"{self.scheme}://{self.host}:{self.port}/{self.service_path}"


class CelerySettings(BaseSettings):
    conf: str = Field("celery_conf", env="CELERY_CONF")
    delivery: dict = {
        "email": "process_email_query",
        "websocket": "process_websocket_query",
    }


class Settings(BaseSettings):
    mongo: MongoSettings = MongoSettings()
    rabbit: RabbitSettings = RabbitSettings()
    notification_app: NotificationAppSettings = NotificationAppSettings()
    celery: CelerySettings = CelerySettings()


settings = Settings.parse_file(DEFAULT_CONFIG_PATH)
