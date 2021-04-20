import pathlib

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()

BASE_DIR = pathlib.Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = BASE_DIR / "config" / "websocket.json"


class AuthSettings(BaseSettings):
    debug: int = Field(1, env="AUTH_DEBUG")
    debug_user_id: str = Field("user-12345", env="DEBUG_USER_ID")
    scheme: str = Field("http")
    host: str = Field("localhost", env="AUTH_HOST")
    port: int = Field(8000, env="AUTH_PORT")
    pubkey_path: str = Field("api/v1/pubkey", env="AUTH_PUBKEY_PATH")

    def get_uri(self):
        return f"{self.scheme}://{self.host}:{self.port}/{self.pubkey_path}"


class Settings(BaseSettings):
    auth: AuthSettings = AuthSettings()

    sleep_time: int = Field(10)


settings = Settings.parse_file(DEFAULT_CONFIG_PATH)
