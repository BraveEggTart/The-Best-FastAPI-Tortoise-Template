import jwt

# from app.schemas.jwt import JWTPayloadSchema
from app.config import settings


def create_token(data):
    encoded_jwt = jwt.encode(
        payload=data.model_dump(),
        key=settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt
