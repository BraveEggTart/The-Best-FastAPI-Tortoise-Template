from typing import Optional, Generic, TypeVar, Union, List

from pydantic import BaseModel

DataT = TypeVar("DataT")


class MetaModel(BaseModel):
    code: Optional[int] = 200
    msg: Optional[str] = "请求响应成功"
    total: Optional[int] = 1
    page: Optional[int] = 1
    size: Optional[int] = 1
    pages: Optional[int] = 1


class Success(MetaModel, Generic[DataT]):
    code: Optional[int] = 200
    msg: Optional[str] = "请求响应成功"
    data: Optional[Union[DataT, List, None, str]] = None


class Fail(MetaModel, Generic[DataT]):
    code: int = 400
    msg: Optional[str] = "请求响应失败"
    data: Optional[Union[DataT, List, None, str]] = None
