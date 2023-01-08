import discord
from typing import Literal
from controller import FateServantController
from model import RedisDatabase
from utils import Log
from model.enumerator import ServantMessageButtonType as ButtonType


class ServantOptionsMenu(discord.ui.View):
    
    def __init__(self: object, bot_client: discord.client) -> None:
        super().__init__()
        self.value = None
        self.database = RedisDatabase.get_database()
        self.logger = Log.get_logger()
        self.bot = bot_client
        return
        
    @discord.ui.button(label='<', style=discord.ButtonStyle.blurple)
    async def backward_button(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        self.logger.info('User: {username} - {discriminator_id} | Clicked: Backward Button'.format(username=button.user.name,
                                                                                                  discriminator_id=button.user.discriminator))
        await button.response.defer()
        await self.change_servant_in_message(button,
                                             button_action=ButtonType.BackwardButton)
    
    @discord.ui.button(label='O', style=discord.ButtonStyle.blurple)
    async def check(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        self.logger.info('User: {username} - {discriminator_id} | Clicked: Check Button'.format(username=button.user.name,
                                                                                                  discriminator_id=button.user.discriminator))
        await button.response.defer()
        await button.message.edit(view=None)
        search_id = f'{button.message.id}_{button.guild_id}'
        result_of_deletion = await FateServantController.delete_servant_search(search_id)
        if result_of_deletion is False:
            self.logger.critical("The search file with ID ({file_id}) can't be found")
        
    @discord.ui.button(label='>', style=discord.ButtonStyle.blurple)
    async def forward(self, button: discord.ui.Button, interaction: discord.Interaction) -> None:
        self.logger.info('User: {username} - {discriminator_id} | Clicked: Forward Button'.format(username=button.user.name,
                                                                                                  discriminator_id=button.user.discriminator))
        await button.response.defer()
        await self.change_servant_in_message(button, 
                                             button_action=ButtonType.ForwardButton)
        
    async def change_servant_in_message(self: object, button: discord.ui.Button, button_action: ButtonType) -> None:
        search_id = f'{button.message.id}_{button.guild_id}'
        search_results = self.get_search_results_info(search_id)
        new_index = ServantOptionsMenu.get_new_servant_index_by(button_action, search_results)
        message = self.bot.get_partial_message(button.message.id)
        next_servant_data = search_results['servant_search_results'][new_index]
        self.database.set_data(search_id, new_index)
        await FateServantController.send_servant_message(self.bot, next_servant_data, message)

    def get_search_results_info(self: object, search_id: str) -> dict:
        message_search_results = FateServantController.get_search_results_if_exists(search_id)
        message_servant_index = int(self.database.get_data(search_id))
        return {'actual_servant_index': message_servant_index,
                'servant_search_results': message_search_results}
    
    @staticmethod
    def get_new_servant_index_by(button: ButtonType, search_results):
        if button is ButtonType.ForwardButton:
            return (search_results['actual_servant_index'] + 1) if search_results['actual_servant_index'] < (len(search_results['servant_search_results']) - 1) else search_results['actual_servant_index']
        elif button is ButtonType.BackwardButton:
            return (search_results['actual_servant_index'] - 1) if search_results['actual_servant_index'] > 0 else 0
    