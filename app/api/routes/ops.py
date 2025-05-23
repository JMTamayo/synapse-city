from fastapi import APIRouter, status

from app.services.ops import run
from app.models.ops import TunnelConditionsRequest, TunnelOperationResponse

ops_router: APIRouter = APIRouter(
    prefix="/operations",
    tags=["Operations"],
)


@ops_router.post(
    path="/tunnel",
    response_model=TunnelOperationResponse,
    status_code=status.HTTP_201_CREATED,
)
def get_tunnel_operation_suggestions(
    request: TunnelConditionsRequest,
) -> TunnelOperationResponse:
    return run(request)
