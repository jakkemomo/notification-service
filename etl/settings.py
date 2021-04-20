import logging
import pathlib

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()

BASE_DIR = pathlib.Path(__file__).parent
DEFAULT_CONFIG_PATH = BASE_DIR / "config" / "etl_config.json"
logger = logging.getLogger(__name__)


class TemplateStorageSettings(BaseSettings):
    host: str = Field("localhost", env="TEMPLATE_STORAGE_HOST")
    port: int = Field(8899, env="TEMPLATE_STORAGE_PORT")


class AuthAppSettings(BaseSettings):
    host: str = Field("localhost", env="AUTH_APP_HOST")
    port: int = Field(8080, env="AUTH_APP_PORT")


class BrokerSettings(BaseSettings):
    scheme: str = Field("amqp", env="BROKER_SCHEME")
    host: str = Field("localhost", env="BROKER_HOST")
    port: int = Field(5672, env="BROKER_PORT")


class BackendSettings(BaseSettings):
    scheme: str = Field("redis", env="BACKEND_SCHEME")
    host: str = Field("localhost", env="BACKEND_HOST")
    port: int = Field(6380, env="BACKEND_PORT")


class WebsocketSettings(BaseSettings):
    scheme: str = Field("http", env="WEBSOCKET_SCHEME")
    host: str = Field("localhost", env="WEBSOCKET_HOST")
    port: int = Field(9000, env="WEBSOCKET_PORT")


class CelerySettings(BaseSettings):
    task_routes: dict = {
        "email.*": {"queue": "email"},
        "websocket.*": {"queue": "websocket"},
    }


class MailingServiceSettings(BaseSettings):
    host: str = Field("email-smtp.us-east-2.amazonaws.com", env="MAIL_HOST")
    port: int = Field(587, env="MAIL_PORT")
    user: str = Field("AKIAQGMSS53BTSOODWER", env="MAIL_USER")
    password: str = Field(
        "BH8gQTLp7cuwIhyOHNm2YMCYOqtAZUALjNtfICIDxGx2", env="MAIL_PASS"
    )
    sender: str = Field("icode.mailing@gmail.com", env="MAIL_SENDER")
    sender_name: str = Field("Yandex Notify", env="MAIL_SENDER_NAME")


class Settings(BaseSettings):
    auth_app: AuthAppSettings = AuthAppSettings()
    mail_service: MailingServiceSettings = MailingServiceSettings()
    template_storage: TemplateStorageSettings = TemplateStorageSettings()
    broker: BrokerSettings = BrokerSettings()
    backend: BackendSettings = BackendSettings()
    celery: CelerySettings = CelerySettings()
    websocket: WebsocketSettings = WebsocketSettings()


settings = Settings.parse_file(DEFAULT_CONFIG_PATH)
