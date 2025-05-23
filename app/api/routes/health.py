from fastapi import APIRouter

from app.models.server import ServerReady

health_router: APIRouter = APIRouter(
    prefix="/server",
    tags=["Server"],
)


@health_router.get(
    path="/health",
    response_model=ServerReady,
)
def verify_server_status() -> ServerReady:
    """
    Returns a simple status response indicating that the server is running and ready to accept requests. If the server is not running, an error will be returned.
    """
    return ServerReady()
