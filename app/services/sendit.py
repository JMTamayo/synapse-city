from pydantic import BaseModel
import requests
from typing import List

from app.config.conf import CONFIG


class SendItHandler(BaseModel):
    url: str

    def __init__(self):
        super().__init__(
            url=f"{CONFIG.SENDIT_HOST}{CONFIG.SENDIT_PATH_BASE}",
        )

    def send_email(self, recipients: List[str], body: str, subject: str):
        for recipient in recipients:
            try:
                response = requests.post(
                    self.url,
                    json={"recipient": recipient, "subject": subject, "body": body},
                )
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                # Log the error but continue with other recipients
                print(f"Failed to send email to {recipient}: {str(e)}")
                continue
