import json
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Request

from api.dependencies.container import AppContainer, build_container

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/github", status_code=202)
async def github_webhook(
    request: Request,
    container: Annotated[AppContainer, Depends(build_container)],
    x_github_event: Annotated[str | None, Header(alias="X-GitHub-Event")] = None,
    x_hub_signature_256: Annotated[str | None, Header(alias="X-Hub-Signature-256")] = None,
) -> dict[str, str]:
    body = await request.body()

    if not container.signature_validator.validate(body, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

    if not x_github_event:
        raise HTTPException(status_code=400, detail="Missing X-GitHub-Event header")

    payload = json.loads(body)
    async with container.session_factory() as session:
        use_case = container.webhook_use_case(session)
        result = await use_case.execute(x_github_event, payload)

    return {"status": "accepted", "message": result.message}
