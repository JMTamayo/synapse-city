from pydantic import BaseModel
from datetime import datetime


class ServerReady(BaseModel):
    message: str
    timestamp: datetime

    def __init__(self):
        super().__init__(
            message="The server is running and it is ready to accept requests",
            timestamp=datetime.now(),
        )
