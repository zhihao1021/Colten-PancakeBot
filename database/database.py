from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from config import DB_URL, DB_NAME
from discord_oauth import StorageData
from schemas import (
    StockData,
    UserDataRelation,
    TradeBuyQueueRelation,
    TradeSellQueueRelation,
)

client = AsyncIOMotorClient(DB_URL)

DB = client[DB_NAME]


async def setup_db():
    await init_beanie(
        database=DB,
        document_models=[
            StorageData,
            StockData,
            UserDataRelation,
            TradeBuyQueueRelation,
            TradeSellQueueRelation,
        ]
    )
