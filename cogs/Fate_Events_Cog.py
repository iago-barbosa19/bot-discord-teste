from discord.ext import commands, tasks
from utils import Log
from model import RedisDatabase
from controller import FateEventsController
import discord, datetime


class FateEvents(commands.Cog):
    
    def __init__(self: object, bot: discord.client) -> None:
        self.bot = bot
        self.database: RedisDatabase = RedisDatabase.get_database()
        self.controller: FateEventsController = FateEventsController()
        self.logger: Log = Log.get_logger()
        self.verify_current_event_and_post_it.start()
    
    # """hours= 24"""
    @tasks.loop(hours=12)
    async def verify_current_event_and_post_it(self: object) -> None:
        """
        This method does the verification of the current event's of the FGO game, and if there is any event it will be posted

        Args:
            self (object): The object itself
        """
        try:
            self.logger.info("Running verification of events of FGO Game")
            actual_events = self.controller.get_events_from(datetime.datetime.now())
            if len(actual_events) >= 1:
                await self.controller.post_events(actual_events, self.bot)
        except Exception as ex:
            self.logger.error(ex)

    @verify_current_event_and_post_it.before_loop
    async def before_verify_current_event_and_post_it(self:object) -> None:
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot):
    await bot.add_cog(FateEvents(bot))
    