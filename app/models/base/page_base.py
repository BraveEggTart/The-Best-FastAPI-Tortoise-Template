from typing import Optional
from pydantic import BaseModel, Field


class PageBase(BaseModel):
    page: Optional[int] = Field(1, description="当前页码", examples=[1])
    size: Optional[int] = Field(50, description="每页数量", examples=[50])
