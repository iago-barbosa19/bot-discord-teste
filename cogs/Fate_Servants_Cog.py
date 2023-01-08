import discord, jsonpickle, asyncio
from time import sleep as wait
from model import FateGOServant as FateServant
from discord.ext import commands, tasks
from controller import FateServantController
from utils import Log
from model import RedisDatabase


class FateServants(commands.Cog):
    
    def __init__(self: object, bot):
        self.bot = bot
        self.database: RedisDatabase = RedisDatabase.get_database()
        self.logger: Log = Log.get_logger()
    
    @commands.command(name='s_servo', aliases=['show_servo'])
    async def search_servants(self: object, client: discord.Client, *args) -> None:
        self.logger.info(f'Command: {client.command.aliases[0]}|Activator: {client.author.name}|Args: {", ".join(args)}')
        servant_name = ' '.join(args)
        servants_data = await FateServantController.retrieve_servants_data(servant_name)
        if len(servants_data) > 0:
            message_id = await self.send_message_with_search_result_in(client.channel, servants_data)
            self.save_search_results(message_id, client.guild.id, servants_data)
        else:
            self.logger.warn(f'No servant found --- Servant wanted: {servant_name}')
            await client.send('Servo não encontrado')

    async def send_message_with_search_result_in(self: object, channel, servant_data: FateServant) -> str:
        message_sender_task = asyncio.create_task(FateServantController.send_message_and_retrieve_id(channel, servant_data))
        return await asyncio.gather(message_sender_task)

    async def save_search_results(self: object, message_id: str,  guild_id: str, servants_data: tuple):
        search_id = f'servant_search:{message_id[0]}_{guild_id}'
        self.database.set_data(search_id, 0)
        save_search_results_task = asyncio.create_task(self.save_temp_search_result(servants_data, search_id))
        await asyncio.gather(save_search_results_task)

    async def save_temp_search_result(self: object, data: dict, search_id: str) -> None:
        try:
            temp_archive_name = f'{search_id}.json'
            data_to_save = tuple(jsonpickle.encode(tuple(FateServantController.mount_servant_object(servant) for servant in data)))
            with open(f'./temp/{temp_archive_name}', 'w') as temp:
                temp.writelines(data_to_save)
        except Exception as ex:
            self.logger.error('Error saving the temporary data of the search', ex)
    
    async def finish_servant_search(self: object, search_id: str, client: discord.client) -> None:
        try:
            await FateServantController.delete_servant_search(search_id)
            teste = client.channel.get_partial_message(search_id.split('_')[0])
            await teste.edit(view=None)
        except Exception as ex: 
            self.logger.error('Error trying to finish the servant search', ex)

        
async def setup(bot: commands.Bot):
    await bot.add_cog(FateServants(bot))
    