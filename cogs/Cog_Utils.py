from discord.ext import commands, tasks
from discord import Client
import discord #, jsonpickle, asyncio
from controller import CogUtilsController
from utils import Log


class Cog_Utils(commands.Cog):
    
    def __init__(self: object, bot) -> None:
        self.bot = bot
        self.logger: Log = Log.get_logger()
        self.controller: CogUtilsController = CogUtilsController()
    
    @commands.Cog.listener()
    async def on_guild_join(self: object, guild: discord.Guild) -> None:
        try:
            await self.controller.save_guild(guild.id, guild.name, guild.system_channel.id)
            await guild.system_channel.send('Olá, obrigado por me utilizar! Para utilizar meus comandos, use o prefixo "!", e caso queira saber os comandos, utilize "!help"')
        except RuntimeWarning as ex:
            self.logger.error('Error trying to join a guild', ex)
    
    @commands.Cog.listener()
    async def on_guild_remove(self: object, guild: discord.Guild) -> None:
        try:
            await self.controller.delete_guild(guild.name)
        except Exception as ex:
            self.logger.error('Error trying to leave a guild', ex)
        
    @commands.command(name='help')
    async def get_help(self: object, client: discord.Client) -> None:
        await self.controller.send_commands_message(client)

    @commands.command(name='change_event_channel', aliases=['ch_event_channel', 'ch_events'])
    async def change_events_channel(self: object, client: discord.Client, *args) -> None:
        channel_name = ' '.join(args)
        channel_id = await self.controller.get_channel_id_of(channel_name, client.guild.text_channels)
        await self.controller.change_channel_of_events(client.guild.name, channel_id)

    @commands.command(name='cottation_of')
    async def conversor_of_coins(self: object, client,  *args) -> None:
        coin, coin_to_convert = args[0], args[1]
        cottation = self.controller.get_actual_cottation_of(coin, coin_to_convert)
        await client.send(cottation)
        pass
    
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Cog_Utils(bot))
    