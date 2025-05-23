from pydantic import BaseModel, Field

from app.config.conf import CONFIG


class TunnelLocation(BaseModel):
    lat: float = Field(
        default=CONFIG.TUNNEL_LATITUDE,
        description="The latitude of the tunnel location. This is a hardcoded value, you don't need to provide it",
    )
    lon: float = Field(
        default=CONFIG.TUNNEL_LONGITUDE,
        description="The longitude of the tunnel location. This is a hardcoded value, you don't need to provide it",
    )


class WeatherStatus(BaseModel):
    main: str
    description: str


class WeatherMainInfo(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    humidity: int


class WeatherWindInfo(BaseModel):
    speed: float
    deg: int
    gust: float


class WeatherCloudsInfo(BaseModel):
    all: int


class OpenWeatherResponse(BaseModel):
    weather: list[WeatherStatus]
    main: WeatherMainInfo
    visibility: int
    wind: WeatherWindInfo
    clouds: WeatherCloudsInfo
    name: str
