import requests

from app.config.conf import CONFIG
from app.models.weather import OpenWeatherResponse, TunnelLocation


def get_weather_information(location: TunnelLocation) -> OpenWeatherResponse:
    """
    Get the weather information for the tunnel location.
    This tool does not require any arguments because it has been hardcoded to get the weather information for the tunnel location.
    """

    params = {
        "lat": location.lat,
        "lon": location.lon,
        "appid": CONFIG.OPENWEATHER_API_KEY.get_secret_value(),
        "units": CONFIG.OPENWEATHER_API_UNITS,
        "lang": CONFIG.OPENWEATHER_API_LANGUAGE,
    }

    url: str = f"{CONFIG.OPENWEATHER_API_HOST}{CONFIG.OPENWEATHER_API_PATH}"

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        return OpenWeatherResponse.model_validate(data)

    except requests.exceptions.RequestException as e:
        if response.status_code == 404:
            raise ValueError("City not found by coordinates")
        elif response.status_code == 401:
            raise ValueError("Invalid API key")
        else:
            raise requests.RequestException(f"Failed to fetch weather data: {str(e)}")
