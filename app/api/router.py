from fastapi import APIRouter

from app.api.routes.health import health_router
from app.api.routes.ops import ops_router

server_router: APIRouter = APIRouter()

server_router.include_router(health_router)
server_router.include_router(ops_router)
