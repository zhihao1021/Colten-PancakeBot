from pydantic import BaseModel, Field
from datetime import datetime, UTC


class TradeBase(BaseModel):
    id: str = Field(
        title="Trade ID",
        description="Trade unique id"
    )
    target_price: int = Field(
        title="Trade Price",
        description="Trade target price pre stock set by user"
    )
    stock_code: int = Field(
        title="Stock Code",
        description="Stock's code"
    )
    stock_count: int = Field(
        title="Stock Count",
        description="Trade count set by user"
    )
    timestamp: float = Field(
        default_factory=datetime.now(UTC).timestamp,
        title="Create Timestamp",
        description="Timestamp as this trade create"
    )


class TradeCreate(BaseModel):
    target_price: int = Field(
        title="Trade Price",
        description="Trade target price pre stock set by user"
    )
    stock_code: int = Field(
        title="Stock Code",
        description="Stock's code"
    )
    stock_count: int = Field(
        title="Stock Count",
        description="Trade count set by user"
    )
