from typing import Optional, Generic, TypeVar

from pydantic import BaseModel

DataT = TypeVar("DataT")


class Success(BaseModel, Generic[DataT]):
    code: Optional[int] = 200
    msg: Optional[str] = "请求响应成功"
    data: Optional[DataT] = None


class Fail(BaseModel, Generic[DataT]):
    code: int = 400
    msg: Optional[str] = "请求响应失败"
    data: Optional[DataT]


class SuccessExtra(BaseModel, Generic[DataT]):
    code: int = 200
    msg: Optional[str] = "请求响应成功"
    data: Optional[DataT]
    total: int
    page: int
    size: int
    pages: int
