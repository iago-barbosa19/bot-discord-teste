from discord.ext import commands, tasks
from utils import Log
from model import RedisDatabase
from controller import FateEventsController
import discord, datetime


class FateEvents(commands.Cog):
    
    def __init__(self: object, bot: discord.client) -> None:
        self.bot = bot
        self.database: RedisDatabase = RedisDatabase.get_database()
        self.controller = FateEventsController()
        self.logger = Log.get_logger()
        self.verify_current_event_and_post_it.start()
    
    # """hours= 24"""
    @tasks.loop(hours=12)
    async def verify_current_event_and_post_it(self: object) -> None:
        try:
            self.logger.info("Running verification of events of FGO Game")
            actual_events = self.controller.get_events_from(datetime.datetime(year=2022, month=12, day=1))
            if len(actual_events) >= 1:
                await self.controller.post_actual_events(actual_events, self.bot)
        except Exception as ex:
            self.logger.error(ex)

    @verify_current_event_and_post_it.before_loop
    async def before_verify_current_event_and_post_it(self:object) -> None:
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot):
    await bot.add_cog(FateEvents(bot))
    