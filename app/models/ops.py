from pydantic import BaseModel
from enum import Enum
from app.models.weather import OpenWeatherResponse


class TunnelConditionsRequest(BaseModel):
    co2_concentration: float | None = None
    luminosity_at_tunnel_exit: float | None = None


class DecisionType(str, Enum):
    CONTINUE_NORMALY = "CONTINUE_NORMALY"
    PARTIALLY_RESTRICT = "PARTIALLY_RESTRICT"
    CLOSE = "CLOSE"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TunnelOperationResponse(BaseModel):
    decision: DecisionType
    risk_level: RiskLevel
    details: str
    weather_information: OpenWeatherResponse
