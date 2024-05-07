from discord import ApplicationContext, Bot, Member, SlashCommandGroup

from math import log10
from typing import Optional

from schemas import UserDataRelation

from .base import GroupCog


class EconomySystem(GroupCog):
    group = SlashCommandGroup(
        name="eco",
        description="Economy system"
    )

    @group.command(
        name="money",
        description="查詢自己或別人有多少錢"
    )
    async def query_money(
        self,
        ctx: ApplicationContext,
        *,
        target: Optional[Member] = None
    ):
        is_self = target is None
        if is_self:
            target = ctx.author

        target_data = await UserDataRelation.get(target.id)
        money = 0 if target_data is None else target_data.money
        username = "你" if is_self else target.display_name

        await ctx.respond(f"{username}目前有 {money} 元！" if money else f"{username}目前有 0 元，哈哈")

    @group.command(
        name="pancake",
        description="查詢自己或別人有幾個鬆餅"
    )
    async def query_pancake(
        self,
        ctx: ApplicationContext,
        *,
        target: Optional[Member] = None
    ):
        is_self = target is None
        if is_self:
            target = ctx.author

        target_data = await UserDataRelation.get(target.id)
        pancake = 0 if target_data is None else target_data.pancake
        username = "你" if is_self else target.display_name

        await ctx.respond(f"為什麼{username}的鬆餅數量是負數？？？{username}是不是一直在想辦法從系統偷到更多鬆餅"
                          if pancake < 0 else f"{username}現在擁有 {pancake} 個鬆餅")

    @group.command(
        name="exp",
        description="查詢自己或別人的經驗值"
    )
    async def query_experience(
        self,
        ctx: ApplicationContext,
        *,
        target: Optional[Member] = None
    ):
        is_self = target is None
        if is_self:
            target = ctx.author

        target_data = await UserDataRelation.get(target.id)
        experience = 0 if target_data is None else target_data.experience
        username = "你" if is_self else target.display_name

        await ctx.respond(f"{username}目前擁有 {experience} 點經驗值！一次可以釣起 {int(log10(10 + experience))} 隻魚")

    @group.command(
        name="exchange_pancake",
        description="把鬆餅拿去換錢"
    )
    async def exchange_pancake(
        self,
        ctx: ApplicationContext,
        *,
        num: int
    ):
        # Get user data
        user_id = ctx.author.id
        user = await UserDataRelation.get(user_id)

        # Check whether user's pancake greater than exchange num
        if num > user.pancake:
            await ctx.respond("你根本沒有這麼多的鬆餅，不要以為我不知道！")
            return

        # Check whether exchange pancake equal to zero
        if num == 0:
            await ctx.respond("你沒有要換任何鬆餅那你找我幹嘛？，你結帳+10")
            return

        # Check whether exchange pancake less than zero
        if num < 0:
            await ctx.respond(f"你為什麼要輸入負數？你完蛋了，我要把你輸入的東西變成你鬆餅增加的數量，所以你的鬆餅數量增加了 {num} 個")

            # Update user's pancake
            user.pancake += num

            # Save modify
            await user.save()
            return

        # Update user's pancake and money
        user.pancake -= num
        user.money += 100 * num

        # Save modify
        await user.save()

        # Respond
        await ctx.respond(f"兌換成功！你兌換了 {num} 個鬆餅並獲得 {100 * num} 元")

    @group.command(
        name="prize",
        description="查詢目前獎池內有多少錢"
    )
    async def query_prize(
        self,
        ctx: ApplicationContext,
    ):
        target_data = await UserDataRelation.get(self.bot.user.id)
        prize = 0 if target_data is None else target_data.money

        await ctx.respond(f"獎池內目前有 {prize} 元！")


def setup(bot: Bot):
    bot.add_cog(EconomySystem(bot=bot))
