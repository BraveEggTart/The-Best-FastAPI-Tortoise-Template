import jwt
import logging

from fastapi import Header, HTTPException

from app.config import settings

logger = logging.getLogger(__name__)


def jwt_token(
    Authorization: str = Header("", description="token验证"),
) -> None:
    try:
        token = Authorization.replace("Bearer ", "")
        jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
    except jwt.DecodeError as jd:
        raise HTTPException(status_code=401, detail=str(jd))
    except jwt.ExpiredSignatureError as jes:
        raise HTTPException(status_code=401, detail=str(jes))
    except ValueError as v:
        raise HTTPException(status_code=401, detail=str(v))
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))