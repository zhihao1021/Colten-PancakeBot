from discord import ApplicationContext, Bot, Member
from discord.ext.commands import Cog, slash_command

from math import log10
from random import choices, randint, random, uniform

from config import BOT_GUARD_ID
from const import FISH_LIST
from schemas import UserDataRelation

DISPLAY_GAO_RUI_RATIO = 90
GAO_RUI_RATIO = len(FISH_LIST) / (DISPLAY_GAO_RUI_RATIO - 1)
ONE_LIST = tuple(map(lambda _: 1, range(len(FISH_LIST))))


def calculate_length_and_money(fish_name: str) -> tuple[str, float, float]:
    fish_length = uniform(0, 1000)
    fish_price = fish_length * uniform(0.03, 1)

    return fish_name, fish_length, fish_price


class FishingSystem(Cog):
    bot: Bot

    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot

    @slash_command(
        name="fishing",
        description=f"釣起一隻魚，目前釣起高睿的機率為 1/{DISPLAY_GAO_RUI_RATIO}!"
    )
    async def finshing(
        self,
        ctx: ApplicationContext,
    ):
        # Get user data
        user_id = ctx.author.id
        user = (await UserDataRelation.get(user_id)) or UserDataRelation(id=user_id)

        # Calculate fishing count
        fishing_count = int(log10(10 + user.experience))

        # Choice fish
        fish_result = tuple(choices(
            FISH_LIST + ("高睿",),
            weights=ONE_LIST + (GAO_RUI_RATIO,),
            k=fishing_count
        ))
        # Convert result from name to [name, length, price]
        convert_result = tuple(map(
            calculate_length_and_money,
            fish_result
        ))

        # Check if get prize
        get_prize = "高睿" in fish_result
        # Check if get tax
        get_tax = random() < 0.15

        # Calculate total money that user get
        total_money = int(sum(map(lambda v: v[2], convert_result)))
        prize_money = 0
        tax_money = 0

        # If get prize, add prize pool money to user's money
        if get_prize:
            bot_data = await UserDataRelation.get(self.bot.user.id)
            if bot_data is not None:
                prize_money = bot_data.money

                await bot_data.set({
                    UserDataRelation.money: 0
                })
            total_money += prize_money

        # If get tax, take user's money to guard's money
        if get_tax:
            tax_money = round(uniform(0, abs(total_money / 5)))
            total_money -= tax_money

            guard = (await UserDataRelation.get(BOT_GUARD_ID)) or UserDataRelation(id=BOT_GUARD_ID)
            guard.money += tax_money
            await guard.save()

        # Save modify
        user.money += total_money
        await user.save()

        # Output
        responses = []
        if get_prize:
            context = f"#【公告】恭喜 {ctx.author.mention} 釣到了高睿，將獎池裡面的 {prize_money} 元全部拿走！"
            responses.append(context)
        if get_tax:
            context = f"由於 {ctx.author.mention} 使用了國家的海域，遭到了海巡署長的課稅，你的釣魚所得被收取了 {tax_money} 元的稅金"
            responses.append(context)

        if fishing_count > 1:
            string_result = tuple(map(
                lambda v: f"{format(v[1], '.2f')}公分長的{v[0]}",
                convert_result
            ))
            context = f"你共釣起了 {fishing_count} 隻魚，他們分別是{'、'.join(string_result)}"
        else:
            context = f"你釣起了{format(convert_result[0][1], '.2f')}公分長的{convert_result[0][0]}"
        responses.append(context)
        responses.append(f"最終獲得{total_money}元")

        # Respond
        await ctx.respond("\n".join(responses))

    @slash_command(
        name="steal",
        description="嘗試偷走某個人的錢"
    )
    async def steal(
        self,
        ctx: ApplicationContext,
        *,
        target: Member
    ):
        # Check whether author equal to target
        if ctx.author.id == target.id:
            await ctx.respond("你偷你自己幹嘛？？你結帳 +10")
            return

        # Check whether target is self (prize pool)
        if target.id == self.bot.user.id:
            await ctx.respond("你偷我？？？獎池你也敢偷，你結帳+10")
            return

        # Get user data
        user_id = ctx.author.id
        user = (await UserDataRelation.get(user_id)) or UserDataRelation(id=user_id)

        # Get target user data
        target_user_id = target.id
        target_user = await UserDataRelation.get(target_user_id)

        # Check whether target user's money greater than zero
        if target_user is None or target_user.money <= 0:
            await ctx.respond("你想偷的人已經負債或沒有錢了！不要再偷他了QQ")
            return

        # Check whether user's money greater than zero
        if user.money < 0:
            await ctx.respond("你現在都負債了還想偷錢R")
            return

        if random() < 0.3:
            # Steal success
            # Calculate steal money and get experience
            steal_money = int(uniform(0, target_user.money / 2))
            add_experience = int(steal_money * uniform(0, 1))

            # Update data
            user.money += steal_money
            user.experience += add_experience

            target_user.money -= steal_money

            # Save modify
            await user.save()
            await target_user.save()

            # Respond
            await ctx.respond("\n".join([
                f"Successful Stealing！你偷走了 {target.display_name} {steal_money} 元",
                f"由於 {ctx.author.mention} 成功偷取別人的財產，獲得了 {add_experience} 點經驗值"
            ]))
            return
        else:
            # Steal failed
            # Calculate loss money and pancake
            loss_money = int(uniform(0, target_user.money / 5))
            add_pancake = randint(0, 10)

            # Update data
            user.money -= loss_money

            target_user.pancake += add_pancake

            bot_data = (await UserDataRelation.get(self.bot.user.id)) or UserDataRelation(id=self.bot.user.id)
            bot_data.money += loss_money

            # Save modify
            await user.save()
            await target_user.save()
            await bot_data.save()

            # Respond
            await ctx.respond("\n".join([
                f"Unsuccessful Stealing，你嘗試偷取 {target.display_name} 的錢失敗，損失了 {loss_money} 元，這些錢將被增加進去獎勵池！",
                f"【公告】由於 {target.display_name} 遭到偷取財產失敗，因此獲得 {add_pancake} 個鬆餅"
            ]))
            return


def setup(bot: Bot):
    bot.add_cog(FishingSystem(bot=bot))
