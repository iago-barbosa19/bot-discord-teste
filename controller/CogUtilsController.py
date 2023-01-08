from discord import Client, Embed
from utils import Log
from model import RedisDatabase
import requests, json


class CogUtilsController:

    def __init__(self: object) -> None:
        self.database: RedisDatabase = RedisDatabase.get_database()
        self.logger: Log = Log.get_logger()

    async def save_guild(self: object, guild_id, guild_name, event_channel_id) -> None:
        self.database.set_data(f'bot:guilds:{guild_name}', guild_id)
        self.database.set_data(f'bot:guilds:{guild_name}:event_channel', event_channel_id)

    async def delete_guild(self: object, guild_name: str) -> None:
        self.database.delete_data(f'bot:guilds:{guild_name}')
        self.database.delete_data(f'bot:guilds:{guild_name}:event_channel')
    
    async def send_commands_message(self: object, discord_client: Client) -> None:
        try:
            commands = self.get_all_commands()
            message = CogUtilsController.mount_help_message(commands)
            await discord_client.send(embed=message)
        except Exception as ex:
            self.logger.error('An error occurred when trying to send help message', ex)

    @staticmethod
    def mount_help_message(commands: tuple) -> Embed:
        message = Embed(color=0xe6b800)
        CogUtilsController.append_commands_to(message, commands)
        return message

    @staticmethod
    def append_commands_to(message, commands) -> None:
        for title, command in commands.items():
            title = title.split(':')[-1].split('-')
            message.add_field(name=' | '.join(title), value=command)

    async def get_channel_id_of(self, channel_name, channels_to_search) -> int:
        channel_found = tuple(filter(lambda channel: channel.name == channel_name, channels_to_search))
        if len(channel_found) > 0:
            return int(channel_found[0].id)
        return None
        
    async def change_channel_of_events(self: object, guild_name,  event_channel_id): 
        self.database.set_data(f'bot:guilds:{guild_name}:event_channel', event_channel_id)
    
    def get_all_commands(self: object) -> tuple:
        try:
            return self.database.get_data_list("bot:commands:*")
        except Exception as ex:
            self.logger.error(ex)

    def get_actual_cottation_of(self: object, coin, coin_to_be_converted) -> str:
        try:
            request_result = requests.get(f'https://economia.awesomeapi.com.br/{coin}-{coin_to_be_converted}/1')
            result_in_json = json.loads(request_result.content.decode('utf-8'))[0]
            return f'{result_in_json["code"]} to {result_in_json["codein"]}: {result_in_json["high"]}'
        except Exception as ex:
            self.logger(ex)
        