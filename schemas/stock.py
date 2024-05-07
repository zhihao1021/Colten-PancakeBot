from beanie import Document
from pydantic import BaseModel, Field

from typing import Optional


class FieldInfo(BaseModel):
    name: str = Field(
        default="",
        title="Name",
        description="Field's title"
    )
    value: str = Field(
        default="",
        title="Value",
        description="Field's description"
    )
    inline: bool = Field(
        default=False,
        title="Embed Inline",
        description="Whether display inline in discord embed"
    )


class StockInfo(BaseModel):
    title: str = Field(
        default="",
        title="Title",
        description="Company's name"
    )
    url: Optional[str] = Field(
        default=None,
        title="Url",
        description="Company's url"
    )
    image: Optional[str] = Field(
        default=None,
        title="Image url",
        description="Company's image"
    )
    thumbnail: Optional[str] = Field(
        default=None,
        title="Thumbnail",
        description="Company's avatar"
    )
    color: int = Field(
        default=0x00b0f4,
        title="Embed's color",
        description="Discord embed's color"
    )
    fields: list[FieldInfo] = Field(
        default=[],
        title="Fields",
        description="Discord embed's fields"
    )


class StockDataOnlyId(BaseModel):
    id: str = Field(alias="_id")


class StockDataOnlyCode(BaseModel):
    code: str


class StockData(Document):
    id: str = Field(
        title="Stock ID",
        description="Stock's unique id"
    )
    code: str = Field(
        title="Stock Code",
        description="Stock's unique code"
    )
    price: int = Field(
        default=1000,
        title="Stock Price",
        description="Stock's current price"
    )
    delta: int = Field(
        default=0,
        title="Stock Delta",
        description="Stock's delta, current price minus last price"
    )
    remain: int = Field(
        default=10000,
        title="Remain Stock",
        description="Stock's remain count"
    )
    info: StockInfo = Field(
        default=StockInfo(),
        title="Stock Info",
        description="Stock's information"
    )
