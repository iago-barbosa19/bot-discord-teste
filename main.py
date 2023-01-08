import os, asyncio
from model import RedisDatabase
from utils import Log
from json import load as json_load
from discord import Intents
from discord.ext import commands

def get_project_infos() -> dict:
    data = None
    with open('appsettings.json', 'r') as configs:
        data = json_load(configs)
        
    return data['bot_configuration'], data['database_configuration'], data['log_configuration']

def initialize_instances(database_configs: dict, log_configs: dict) -> None:
    Log.get_logger(log_configs)
    RedisDatabase.get_database()

async def load_extensions(bot: commands.Bot) -> None:
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not 'Cog_Utils' in filename:
            await bot.load_extension(name=f"cogs.{filename[:-3]}")
    await bot.load_extension(name=f'cogs.Cog_Utils')
    
async def prepare_intents() -> Intents:
    intents = Intents.default()
    intents.message_content = True
    return intents

async def main() -> None:
    intents = await prepare_intents()
    bot = commands.Bot(intents=intents, command_prefix="!", help_command=None)
    bot_configs, database_configs, log_configs = get_project_infos()
    initialize_instances(database_configs, log_configs)
    await load_extensions(bot)
    await bot.start(bot_configs['discord_api_key'])

if __name__ == "__main__":
    asyncio.run(main())
