from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from asyncio import sleep as asleep
from hashlib import md5
from os import urandom
from time import time
from threading import Lock
from typing import Union

from schemas import (
    StockData,
    TradeCreate,
    TradeBuyQueueRelation,
    TradeSellQueueRelation,
    UserDataRelation,
)

from ..oauth import UserDepends


trading_lock = Lock()

MONEY_NOT_ENOUGH = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="your money is not enough"
)
STOCK_NOT_ENOUGH = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="your stocks are not enough"
)
STOCK_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="stock not found"
)

router = APIRouter(
    prefix="/trade",
    tags=["Trade"]
)


def generate_trade_id(user_id: Union[int, str]):
    return md5(f"{user_id}{time()}".encode() + urandom(16)).hexdigest()


@router.post(
    path="/buy",
    status_code=status.HTTP_201_CREATED,
    response_model=TradeBuyQueueRelation
)
async def create_buy_trade(user: UserDepends, create_data: TradeCreate) -> TradeBuyQueueRelation:
    try:
        trading_lock.acquire()

        target_stock = await StockData.find_one(StockData.code == create_data.stock_code)
        if target_stock is None:
            raise STOCK_NOT_FOUND

        total_price = create_data.target_price * create_data.stock_count
        user_data = await UserDataRelation.get(user.id, fetch_links=False)
        stock_code = target_stock.code

        if user_data.money < total_price:
            raise MONEY_NOT_ENOUGH

        if target_stock.price <= create_data.target_price:
            buy_count = min(target_stock.remain, create_data.stock_count)

            create_data.stock_count -= buy_count

            if user_data.stock.get(stock_code) is None:
                user_data.stock[stock_code] = 0
            user_data.money -= target_stock.price * buy_count
            user_data.stock[stock_code] += buy_count

            target_stock.remain -= buy_count

            await target_stock.save()

        user_data.money -= create_data.stock_count * create_data.target_price
        await user_data.save()

        trade_data = TradeBuyQueueRelation(
            id=generate_trade_id(user.id),
            creator=user_data,
            **create_data.model_dump()
        )

        if trade_data.stock_count > 0:
            await trade_data.save()

        return trade_data
    finally:
        trading_lock.release()


@router.post(
    path="/sell",
    status_code=status.HTTP_201_CREATED,
    response_model=TradeSellQueueRelation
)
async def create_buy_trade(user: UserDepends, create_data: TradeCreate) -> TradeSellQueueRelation:
    try:
        trading_lock.acquire()

        target_stock = await StockData.find_one(StockData.code == create_data.stock_code)
        if target_stock is None:
            raise STOCK_NOT_FOUND

        user_data = await UserDataRelation.get(user.id, fetch_links=False)
        stock_code = target_stock.code

        if user_data.stock.get(create_data.stock_code, 0) < create_data.stock_count:
            raise STOCK_NOT_ENOUGH

        if target_stock.price >= create_data.target_price:
            user_data.stock[stock_code] -= create_data.stock_count
            user_data.money += target_stock.price * create_data.stock_count

            target_stock.remain += create_data.stock_count

            await user_data.save()
            await target_stock.save()

            return TradeBuyQueueRelation(
                id=generate_trade_id(user.id),
                creator=user_data,
                **create_data.model_dump()
            )
        trade_data = TradeBuyQueueRelation(
            id=generate_trade_id(user.id),
            creator=user_data,
            **create_data.model_dump()
        )
        await trade_data.save()

        return trade_data
    finally:
        trading_lock.release()
