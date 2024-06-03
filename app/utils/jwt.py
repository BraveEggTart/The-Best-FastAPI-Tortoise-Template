from typing import Dict, Any

import jwt

from app.config import settings


def create_token(data: Dict[str, Any]):
    encoded_jwt = jwt.encode(
        payload=data.copy(),
        key=settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt
