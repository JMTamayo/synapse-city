from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import server_router
from app.config.conf import CONFIG


app: FastAPI = FastAPI(
    title=CONFIG.API_NAME,
    description=CONFIG.API_DESCRIPTION,
    version=CONFIG.API_VERSION,
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace this with your specific origins list
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(server_router)
