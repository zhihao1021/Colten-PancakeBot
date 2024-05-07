from discord import ApplicationContext, Bot, SlashCommandGroup

from schemas import UserDataRelation

from .base import GroupCog


class ItemSystem(GroupCog):
    bot: Bot
    group = SlashCommandGroup(
        name="item",
        description="Item system"
    )

    @group.command(
        name="pay_card",
        description="花費 20 個鬆餅使用一張還債卡，他可以讓你的負債歸 0"
    )
    async def pay_card(
        self,
        ctx: ApplicationContext
    ):
        # Get user data
        user_id = ctx.author.id
        user = await UserDataRelation.get(user_id)

        if user is None or user.pancake < 20:
            await ctx.respond("你的鬆餅數量不足")
            return

        if user.money > 0:
            await ctx.respond("你明明就有錢，諧咖")
            return

        if user.money == 0:
            await ctx.respond("你沒有負債但你也沒有錢，可撥")
            return

        # Update user's money and pancake
        user.money = 0
        user.pancake -= 20

        # Save modify
        await user.save()

        await ctx.respond("你使用了還債卡，讓你的負債歸 0 了！繼續努力，小心偷錢")


def setup(bot: Bot):
    bot.add_cog(ItemSystem(bot=bot))
