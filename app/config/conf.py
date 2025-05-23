from pydantic_settings import BaseSettings
from pydantic import SecretStr
from pathlib import Path
import tomllib

with open(Path(__file__).parent.parent.parent / "pyproject.toml", "rb") as f:
    pyproject = tomllib.load(f)

    API_VERSION = pyproject["project"]["version"]
    API_DESCRIPTION = pyproject["project"]["description"]


class Config(BaseSettings):
    API_NAME: str = "Synapse City"
    API_DESCRIPTION: str = API_DESCRIPTION
    API_VERSION: str = API_VERSION

    GEMINI_API_KEY: SecretStr
    GEMINI_MODEL: str
    GEMINI_TEMPERATURE: float

    OPENWEATHER_API_KEY: SecretStr
    OPENWEATHER_API_HOST: str
    OPENWEATHER_API_PATH: str
    OPENWEATHER_API_LANGUAGE: str
    OPENWEATHER_API_UNITS: str

    TUNNEL_LATITUDE: float
    TUNNEL_LONGITUDE: float


CONFIG: Config = Config()
