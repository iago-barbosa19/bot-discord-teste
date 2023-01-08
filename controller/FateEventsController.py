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
        """
        This method get events from Atlas Academy API with a range of date that is passed as a parameter

        Args:
            self (object): 
            events_start_date (datetime, optional): The beginning date of the event. Defaults to datetime.datetime.now().
            events_end_date (datetime, optional): The end date of the event. Defaults to datetime.datetime.now().

        Returns:
            tuple: _description_
        """
        try:
            raw_events_file = requests.get('https://api.atlasacademy.io/export/NA/nice_war.json')
            fgo_events_json = json.loads(raw_events_file.content.decode('utf8'))
            actual_events = self.filter_events_from(fgo_events_json, events_start_date, events_end_date)
            actual_events = tuple(FateGOEvent(  id=event['id'],
                                                name=event['eventName'],
                                                start_date=datetime.datetime.fromtimestamp(event['warAdds'][0]['startedAt']),
                                                end_date=datetime.datetime.fromtimestamp(event['warAdds'][0]['endedAt']),
                                                image_path=event['banner']) for event in actual_events)
            return actual_events
        except Exception as ex:
            self.logger.error('Exceção durante a coleta de eventos.', ex)

    def filter_events_from(self: object, fgo_events: tuple, start_date, end_date) -> tuple:
        """
        This method filters the events that are occurring between the given dates

        Args:
            self (object): _description_
            fgo_events (tuple): List of events to apply the filter
            start_date (_type_): The start date to be used as a filter parameter
            end_date (_type_): The end date to be used as a filter parameter

        Returns:
            tuple: An tuple of events that are occurring between the given dates
        """
        events = tuple(filter(lambda event: len(event['warAdds']) > 0 and datetime.datetime.fromtimestamp(event['warAdds'][0]['startedAt']) >= start_date and datetime.datetime.fromtimestamp(event['warAdds'][0]['endedAt']) <= end_date, fgo_events))
        special_events_filtered = tuple(event for event in fgo_events if event['id'] == 9999)[0]['spots'][0]['quests']
        special_events = tuple(filter(lambda event: datetime.datetime.fromtimestamp(event['openedAt']) >= start_date and datetime.datetime.fromtimestamp(event['closedAt']) <= end_date, special_events_filtered))
        return (events + special_events)
    
    async def post_events(self: object, events: tuple, bot) -> None:
        """
        This method is called to post Events

        Args:
            self (object): _description_
            events (tuple): The events that will be posted
            bot (_type_): The discord client
        """
        try:
            guilds = self.get_active_guilds(bot)
            messages = FateEventsController.prepare_messages_about(events)
            await self.send_messages(guilds, messages)
        except Exception as ex:
            self.logger.error('Erro while trying to post events', ex)

    def get_active_guilds(self: object, bot) -> tuple:
        """
        Get the current guilds where the bot is located, and are active.

        Args:
            self (object): _description_
            bot (_type_): _description_

        Returns:
            tuple: tuple of guild's 
        """
        guilds = self.database.get_data_list('bot:guilds:*')
        return tuple(bot.get_guild(int(guild_id)) for guild_id in guilds.values())

    @staticmethod
    def prepare_messages_about(events: tuple) -> list:
        """
        This method create messages about the events, so it can be posted on the Discord Guilds

        Args:
            events (tuple): Tuple of events who's gonna be posted

        Returns:
            list: List of events Embed messages
        """
        messages = []
        for event in events:
            message = Embed(color=0xff8080)
            message.set_image(url=event.image_path)
            message.add_field(name=event.name, value=f'Data de inicio: {event.start_date} - Data de fim do evento: {event.end_date}')
            messages.append(message)
        return messages

    async def send_messages(self: object, guilds: tuple, messages: tuple) -> None:
        """
        Sends the given messages to the given guilds.

        Args:
            self (object): _description_
            guilds (tuple): Guilds who's gonna receive the message
            messages (tuple): Messages who's gonna be sent to the guilds
        """
        for guild in guilds:
            event_channel_id = self.database.get_data(f'bot:guilds:{guild.name}:event_channel')
            channel = guild.get_channel(int(event_channel_id))
            for message in messages:
                await channel.send(embed=message)
                
    
if __name__ == '__main__':
    FateEventsController.get_events()
    