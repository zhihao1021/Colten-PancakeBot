from discord import Embed

from asyncio import gather
from random import randint

from config import BOT_STOCK_CHANGE_IMAGE, BOT_STOCK_CHANGE_THUMBNIAL
from schemas import FieldInfo, StockData


async def update_stocks() -> list[Embed]:
    results = []
    offset = 0
    while True:
        stock_list = await StockData.find_all(
            skip=offset, limit=25
        ).to_list()

        offset += 25
        if len(stock_list) == 0:
            break

        async def modify(stock: StockData) -> FieldInfo:
            limit = int(max(abs(stock.delta / 3), 100))

            stock.delta += randint(-limit, limit)
            stock.price += stock.delta

            await stock.save()

            return FieldInfo(
                name=stock.info.title,
                value=f"目前股市狀況 (1 股價格): {stock.price} 元 (價格變動: {'+' if stock.delta > 0 else ''}{stock.delta})",
                inline=False
            )

        embed_fields = await gather(*tuple(map(modify, stock_list)))

        embed = Embed(
            title="今日股市變動！！！",
            description="投資一定有風險，基金投資有賺有賠，申購前應詳閱公開說明書",
            image=BOT_STOCK_CHANGE_IMAGE,
            thumbnail=BOT_STOCK_CHANGE_THUMBNIAL,
        )
        for field in embed_fields:
            embed.add_field(**field.model_dump())
        results.append(embed)

        if len(stock_list) < 25:
            break
    return results
