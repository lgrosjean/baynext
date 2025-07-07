from typing import Annotated

from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.settings import settings


async def check_token(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Security(
            HTTPBearer(
                description="Bearer token for API access",
            )
        ),
    ],
) -> None:
    if credentials.credentials != settings.ml_api_secret_api_key.get_secret_value():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )
