from model import FateGOEvent, RedisDatabase as Redis
from discord import Embed
from utils import Log
from typing import Literal
import requests, json, datetime


class FateEventsController:

    def __init__(self: object) -> None:
        self.logger: Log = Log.get_logger()
        self.database: Redis = Redis.get_database()
    
    def get_events_from(self: object, events_start_date: datetime = datetime.datetime.now(), events_end_date: datetime = datetime.datetime.now()) -> tuple:
        try:
            raw_events_file = requests.get('https://api.atlasacademy.io/export/NA/nice_war.json')
            fgo_events_json = json.loads(raw_events_file.content.decode('utf8'))
            actual_events = self.get_actual_events_from(fgo_events_json, events_start_date, events_end_date)
            actual_events = tuple(FateGOEvent(  id=event['id'],
                                                name=event['eventName'],
                                                start_date=datetime.datetime.fromtimestamp(event['warAdds'][0]['startedAt']),
                                                end_date=datetime.datetime.fromtimestamp(event['warAdds'][0]['endedAt']),
                                                image_path=event['banner']) for event in actual_events)
            return actual_events
        except Exception as ex:
            self.logger.error('Exceção durante a coleta de eventos.', ex)

    def get_actual_events_from(self: object, fgo_events: tuple, start_date, end_date) -> tuple:
        events = tuple(filter(lambda event: len(event['warAdds']) > 0 and datetime.datetime.fromtimestamp(event['warAdds'][0]['startedAt']) >= start_date and datetime.datetime.fromtimestamp(event['warAdds'][0]['endedAt']) <= end_date, fgo_events))
        special_events_filtered = tuple(event for event in fgo_events if event['id'] == 9999)[0]['spots'][0]['quests']
        special_things = tuple(event for event in special_events_filtered if '2023' in event['name'])
        special_events = tuple(filter(lambda event: datetime.datetime.fromtimestamp(event['openedAt']) >= start_date and datetime.datetime.fromtimestamp(event['closedAt']) <= end_date, special_events_filtered))
        return (events + special_events)
    
    async def post_actual_events(self: object, events: tuple, bot) -> None:
        try:
            guilds = self.prepare_guilds_for_action(bot)
            messages = FateEventsController.prepare_messages_about(events)
            await self.send_messages(guilds, messages)
        except Exception as ex:
            self.logger.error('Erro while trying to post events', ex)

    @staticmethod
    def prepare_messages_about(events: tuple) -> list:
        messages = []
        for event in events:
            message = Embed(color=0xff8080)
            message.set_image(url=event.image_path)
            message.add_field(name=event.name, value=f'Data de inicio: {event.start_date} - Data de fim do evento: {event.end_date}')
            messages.append(message)
        return messages

    async def send_messages(self: object, guilds: tuple, messages: tuple) -> None:
        for guild in guilds:
            event_channel_id = self.database.get_data(f'bot:guilds:{guild.name}:event_channel')
            channel = guild.get_channel(int(event_channel_id))
            for message in messages:
                await channel.send(embed=message)
        
    def prepare_guilds_for_action(self: object, bot):
        guilds = self.get_all_guilds()
        return tuple(bot.get_guild(int(guild_id)) for guild_id in guilds.values())
        
    def get_all_guilds(self: object) -> tuple:
        return self.database.get_data_list('bot:guilds:*')
    
if __name__ == '__main__':
    FateEventsController.get_events()