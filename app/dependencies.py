import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app import models
from app.config import settings
from app.database import get_db
from app.security import ALGORITHM


bearer = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> models.User:
    unauthorized = HTTPException(
        status_code=401,
        detail="Invalid or missing access token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise unauthorized

    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret_key,
            algorithms=[ALGORITHM],
            options={"require": ["exp", "sub"]},
        )

        user_id = int(payload["sub"])

        if user_id <= 0:
            raise unauthorized

    except (InvalidTokenError, ValueError, TypeError):
        raise unauthorized

    user = db.get(models.User, user_id)

    if user is None:
        raise unauthorized

    return user