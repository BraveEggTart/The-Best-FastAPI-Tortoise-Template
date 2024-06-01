from typing import Optional, Generic, TypeVar, Union, List

from pydantic import BaseModel

DataT = TypeVar("DataT")


class MetaModel(BaseModel, Generic[DataT]):
    code: Optional[int] = 200
    msg: Optional[str] = "Request response successful"
    total: Optional[int] = 1
    page: Optional[int] = 1
    size: Optional[int] = 1
    pages: Optional[int] = 1
    data: Optional[Union[DataT, List, None, str]] = None


class Success(MetaModel, Generic[DataT]):
    code: Optional[int] = 200
    msg: Optional[str] = "Request response successful"


class Fail(MetaModel, Generic[DataT]):
    code: int = 400
    msg: Optional[str] = "Request response failed"
