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
        email_content = f"""Dear Operations Team,

The following is the report for the tunnel operation.

Level of risk: {response.risk_level.value}
Decision: {response.decision.value}

{response.details}

Best regards,
Smart City Operations Team.

This email was sent automatically by the Smart City Operations Team using the Synapse City API.
"""

        sendit_handler = SendItHandler()
        sendit_handler.send_email(
            recipients=CONFIG.get_sendit_recipients(),
            body=email_content,
            subject=f"Tunnel Operation Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        )

    return response
