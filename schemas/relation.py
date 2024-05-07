from beanie import BackLink, Document, Link
from pydantic import Field

from .user import UserData
from .trade import TradeBase


class UserDataRelation(UserData, Document):
    trade_buy: list[Link["TradeBuyQueueRelation"]] = []
    trade_sell: list[Link["TradeSellQueueRelation"]] = []

    class Settings:
        name = "UserData"
        max_nesting_depths_per_field = {
            "trade_buy": 1,
            "trade_sell": 1,
        }


class TradeBuyQueueRelation(TradeBase, Document):
    creator: BackLink[UserDataRelation] = Field(
        title="Trade creator",
        description="User that create this trade",
        original_field="trade_buy",
    )

    class Settings:
        name = "TradeBuyQueue"
        max_nesting_depths_per_field = {
            "creator": 1
        }


class TradeSellQueueRelation(TradeBase, Document):
    creator: BackLink[UserDataRelation] = Field(
        title="Trade creator",
        description="User that create this trade",
        original_field="trade_sell",
    )

    class Settings:
        name = "TradeBuyQueue"
        max_nesting_depths_per_field = {
            "creator": 1
        }
