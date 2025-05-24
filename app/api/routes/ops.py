from fastapi import APIRouter, status
from datetime import datetime

from app.services.ops import run
from app.models.ops import (
    TunnelConditionsRequest,
    TunnelOperationResponse,
    DecisionType,
)
from app.services.sendit import SendItHandler
from app.config.conf import CONFIG

ops_router: APIRouter = APIRouter(
    prefix="/operations",
    tags=["Operations"],
)


def create_email_template(content: str) -> str:
    return f"""
Dear Team,

{content}

Best regards,
Smart City Operations Team.
"""


@ops_router.post(
    path="/tunnel",
    response_model=TunnelOperationResponse,
    status_code=status.HTTP_201_CREATED,
)
def get_tunnel_operation_suggestions(
    request: TunnelConditionsRequest,
) -> TunnelOperationResponse:
    response: TunnelOperationResponse = run(request)

    if response.decision.name != DecisionType.CONTINUE_NORMALY.name:
        email_content = f"""Smart City Operations Alert

We have received an important update regarding the tunnel operations that requires your attention.

OPERATION STATUS:
----------------
Risk Level: {response.risk_level.value}
Recommended Action: {response.decision.value}

DETAILED ANALYSIS:
-----------------
{response.details}

NEXT STEPS:
-----------
Please review this information and take appropriate action based on the risk level and recommended decision. If you have any questions or need additional information, please don't hesitate to reach out to the operations team.

Best regards,
Smart City Operations Team

---
This is an automated message from the Smart City Operations System.
For immediate assistance, please contact the operations team.
"""

        sendit_handler = SendItHandler()
        sendit_handler.send_email(
            recipients=CONFIG.get_sendit_recipients(),
            body=email_content,
            subject=f"Tunnel Operation Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        )

    return response
