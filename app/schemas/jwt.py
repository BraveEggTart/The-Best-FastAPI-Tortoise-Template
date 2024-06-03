from pydantic import BaseModel, Field


class LoginSchemas(BaseModel):
    username: str = Field(
        ...,
        description="登录账号",
        examples=["admin",],
    )
    password: str = Field(
        ...,
        description="登陆密码",
        examples=["123456"]
    )


class JWTOutSchema(BaseModel):
    token_type: str = Field(
        ...,
        description="昵称",
        examples=["admin"]
    )
    token: str = Field(
        ...,
        description="Token",
        examples=["a@test.org"]
    )
