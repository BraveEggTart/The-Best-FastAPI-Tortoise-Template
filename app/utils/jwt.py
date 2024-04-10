import jwt

from app.schemas.jwt import JWTPayloadSchema
from app.config import settings


def create_token(data: JWTPayloadSchema):
    encoded_jwt = jwt.encode(
        payload=data.model_dump().copy(),
        key=settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt
