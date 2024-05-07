from discord import (
    ApplicationContext,
    Bot,
    Embed,
    EmbedAuthor,
    EmbedFooter,
    Option,
    SlashCommandGroup
)

from config import BOT_EMBED_FOOTER_TEXT, BOT_EMBED_FOOTER_IMAGE
from schemas import StockData, StockDataOnlyId

from .base import GroupCog


class StockSystem(GroupCog):
    group = SlashCommandGroup(
        name="stock",
        description="Stock system"
    )

    async def get_stock_code_list(self, *args) -> tuple[str]:
        stock_code_list = await StockData.find_all(projection_model=StockDataOnlyId).to_list()
        return tuple(map(lambda stock: stock.id, stock_code_list))

    @group.command(
        name="query",
        description="查詢股票",
        options=[
            Option(
                str,
                name="stock_code",
                description="股票代號",
                required=True,
                autocomplete=get_stock_code_list,
            )
        ]
    )
    async def query(
        self,
        ctx: ApplicationContext,
        stock_code: str
    ):
        stock = await StockData.get(stock_code)
        if stock is None:
            await ctx.respond("根本沒這個股票，搞什麼")
            return

        embed = Embed(
            color=stock.info.color,
            title=stock.info.title,
            url=stock.info.url,
            author=EmbedAuthor(
                name="目前股市"
            ),
            image=stock.info.image,
            thumbnail=stock.info.thumbnail,
            footer=EmbedFooter(
                text=BOT_EMBED_FOOTER_TEXT,
                icon_url=BOT_EMBED_FOOTER_IMAGE
            )
        )
        embed.add_field(
            name="當前股價",
            value=stock.price,
            inline=True
        )
        embed.add_field(
            name="前次漲跌",
            value=stock.delta,
            inline=True
        )
        for field in stock.info.fields:
            embed.add_field(**field.model_dump())

        await ctx.respond(embed=embed)


def setup(bot: Bot):
    bot.add_cog(StockSystem(bot=bot))
