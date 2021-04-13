import logging
import pathlib

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()

BASE_DIR = pathlib.Path(__file__).parent
DEFAULT_CONFIG_PATH = BASE_DIR / "config" / "etl_config.json"
logger = logging.getLogger(__name__)


class TemplateStorageSettings(BaseSettings):
    host: str = Field("localhost", env="AUTH_APP_HOST")
    port: int = Field(8000, env="AUTH_APP_PORT")


class AuthAppSettings(BaseSettings):
    host: str = Field("localhost", env="AUTH_APP_HOST")
    port: int = Field(5000, env="AUTH_APP_PORT")


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


settings = Settings.parse_file(DEFAULT_CONFIG_PATH)