from pydantic import BaseModel


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
    weather: WeatherStatus
    main: WeatherMainInfo
    visibility: int
    wind: WeatherWindInfo
    clouds: WeatherCloudsInfo
    name: str
