from typing import Optional, Generic, TypeVar, Union

from pydantic import BaseModel

DataT = TypeVar("DataT")


class MetaModel(BaseModel, Generic[DataT]):
    code: Optional[int] = 200
    msg: Optional[str] = "请求响应成功"
    data: Optional[Union[DataT, None, str]] = None
    total: Optional[int] = 1
    page: Optional[int] = 1
    size: Optional[int] = 1
    pages: Optional[int] = 1


class Success(MetaModel):
    code: Optional[int] = 200
    msg: Optional[str] = "请求响应成功"


class Fail(MetaModel):
    code: int = 400
    msg: Optional[str] = "请求响应失败"
