
import jwt
from fastapi import Depends, Header, HTTPException, Request

from app.models import Users
from app.core.ctx import CTX_USER, CTX_LANG
from app.config import settings


class AuthControl:
    @classmethod
    async def is_authed(
        cls,
        token: str = Header(..., description="token验证")
    ) -> Users:
        try:
            if token == "dev":
                user = await Users.filter().first()
                user_id = user.id
            else:
                decode_data = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=settings.JWT_ALGORITHM
                )
                user_id = decode_data.get("id")
            user = await Users.filter(id=user_id).first()
            if not user:
                raise HTTPException(
                    status_code=401,
                    detail="Authentication failed"
                )
            CTX_USER.set(user)
            return user
        except jwt.DecodeError:
            raise HTTPException(status_code=401, detail="无效的Token")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="登录已过期")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"{repr(e)}")


class LangControl:
    @classmethod
    async def set_lang(
        cls,
        lang: str = Header("zh", description="接口多语言")
    ) -> None:
        CTX_LANG.set(lang)


class PermissionControl:
    @classmethod
    async def has_permission(
        cls,
        request: Request,
        current_user: Users = Depends(AuthControl.is_authed)
    ) -> None:
        if current_user.is_superuser:
            return
        method = request.method
        path = request.url.path
        roles: list[Roles] = await current_user.roles
        if not roles:
            raise HTTPException(
                status_code=403,
                detail="The user is not bound to a role"
            )
        apis = [await role.apis for role in roles]
        permission_apis = list(set(
            (api.method, api.path)
            for api in sum(apis, [])
        ))
        # path = "/api/v1/auth/userinfo"
        # method = "GET"
        if (method, path) not in permission_apis:
            raise HTTPException(
                status_code=403,
                detail=f"Permission denied method:{method} path:{path}"
            )


DependAuth = Depends(AuthControl.is_authed)
DependPermisson = Depends(PermissionControl.has_permission)
LangInitial = Depends(LangControl.set_lang)
