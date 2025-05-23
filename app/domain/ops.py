from pydantic import BaseModel

from app.models.ops import TunnelConditionsRequest, TunnelOperationResponse
from app.services.ops import TunnelOperationAgent


class TunnelOperationHandler(BaseModel):
    operation_agent: TunnelOperationAgent

    def __init__(self):
        super().__init__(operation_agent=TunnelOperationAgent())

    def analyze_tunnel_operation_conditions(
        self, request: TunnelConditionsRequest
    ) -> TunnelOperationResponse:
        return self.operation_agent.run(request)
