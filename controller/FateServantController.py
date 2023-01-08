from discord import Embed
import discord
from typing import Literal
from model import FateGOServant, RedisDatabase, FateGOServantNoblePhantasm as NoblePhantasm
from utils import Utils, Log
import textblob, os, threading, requests


class FateServantController:

    def __init__(self: object) -> None:
        self.database = RedisDatabase.get_database()
        self.logger = Log.get_logger()
        
    @staticmethod
    async def retrieve_servants_data(*, servant_name: str, url_api: str = 'https://api.atlasacademy.io/nice/NA/servant/search?name={servant_name}') -> dict:
        """retrieve_servant_data
        
        Get data from the servant who's ben passed
        
        Args:
            servant_name (str):
            url_api (str, optional): Defaults to 'https://api.atlasacademy.io/nice/NA/servant/search?name={servant_name}'.

        Returns:
            dict: servant_data
        """
        servant_request = requests.get(url_api.format(servant_name=servant_name))
        return servant_request.json()
    
    @staticmethod
    async def send_message(client : discord.Client, servant_data: Literal['FateGOServant', 'tuple'], message_sent: bool = False) -> Literal['message_id']:
        """send_servant_message

        Send to the guild and channel who's been called a message with servant informations.
        And returns the id of the sent message.
        
        Args:
            - client (discord.client): Discord API Client
            - servant_data (FateGoServant): Data of the servant
            - message_sent (Bool): Sinalizes that the message is whether sent or not. Defaults to False.
        Returns:
            message_sent.id: The Message Id
        """
        from controller import ServantOptionsMenu
        servant: FateGOServant = FateServantController.mount_servant_object(servant_data) if type(servant_data) is not FateGOServant else servant_data
        message: Embed = FateServantController.mount_servant_message(servant)
        option_menu: ServantOptionsMenu = ServantOptionsMenu(client)        
        message_sent: discord.message = await client.send(embed=message, view=option_menu) if message_sent is False else await message_sent.edit(embed=message, view=option_menu)
        return message_sent.id

    @staticmethod
    def mount_servant_object(servant: dict) -> FateGOServant:
        """mount_servant_object

        Factory method to build a FateGOServant object.

        Args:
            servant (dict): Servant data coming out of an json

        Returns:
            FateGOServant: The Fate Servant Object
        """
        return FateGOServant.factory(servant_name = servant['name'], 
                                servant_class = servant['className'],
                                rarity = servant['rarity'],
                                cost = servant['cost'],
                                attributes = {
                                    'max_hp': servant['hpMax'],
                                    'max_atk': servant['atkMax']
                                },
                                cards = servant['cards'],
                                traits = servant['traits'],
                                skills = servant['skills'],
                                noble_phantasm = servant['noblePhantasms'][0],
                                passive_skills = servant['classPassive'],
                                servant_url_image = servant['extraAssets']['charaGraph']['ascension']['4'])

    @staticmethod
    def mount_servant_message(servant: FateGOServant) -> Embed:
        """mount_servant_message

        Mount message about the servant

        Args:
            servant (FateGOServant): Fate Servant

        Returns:
            Embed: The Embed message
        """
        message = Embed(color=0xe6b800)
        message.set_author(name=servant.name, icon_url=servant.servant_url_image)
        message.set_image(url=servant.servant_url_image)
        FateServantController.insert_basic_infos(message, servant)
        FateServantController.insert_servant_skills_on_message(message, 
                                                               [{'Passive Skills': servant.passive_skills}, {'Skills': servant.skills}])
        FateServantController.insert_noble_phantasm_on_message(message, servant.noble_phantasm)
        return message

    @staticmethod
    def insert_basic_infos(message: Embed, servant: FateGOServant) -> None:
        """insert_basic_infos

        Insert basic infos about the servant

        Args:
            message (FateGoServant): Message to insert the infos
            servant (Embed): Servant to catch the Infos
        """
        message.add_field(name='Infos', value=servant.basic_infos)
        
    @staticmethod
    def insert_servant_skills_on_message(message:Embed, servant_skills: tuple) -> None:
        """insert_servant_skills_on_message
        
        Insert the skills of the servant into message

        Args:
            message (Embed): Embed message to insert the skills 
            servant_skills (tuple): Tuple of ServantSkills Object
        """
        passive_skills = threading.Thread(target=FateServantController.insert_skill_on_message, args=(message, dict(servant_skills[0])))
        skills = threading.Thread(target=FateServantController.insert_skill_on_message, args=(message, dict(servant_skills[1])))
        for threads in [skills, passive_skills]:
            threads.start()
            threads.join()
        
    @staticmethod
    def insert_skill_on_message(discord_message: Embed, servant_skills: dict) -> None:
        """insert_skill_on_message

        Translate and insert field skills into message
        
        Args:
            discord_message (Embed): Embed message to insert the infos
            servant_skills (dict): Dictionary of Skills, Index -> Skill name | Value -> Skill infos
        """
        type_of_skill = tuple(servant_skills.keys())[0]
        skill_message_content = ''
        skills = tuple(servant_skills.values())[0]
        for skill in skills:
            skill_effect = textblob.TextBlob(skill.effect).translate(from_lang='eng', to='pt-br')
            skill_message_content += f'**Nome:** {skill.name}\n**Efeito:** {skill_effect}\n**Cooldown:** {skill.cooldown}\n\n'
        discord_message.add_field(name=type_of_skill, value=skill_message_content)
            
    @staticmethod
    def insert_noble_phantasm_on_message(discord_message: Embed, noble_phantasm: NoblePhantasm) -> None:
        """insert_noble_phantasm_on_message

        Insert Noble Phantasm into message
        
        Args:
            discord_message (Embed): Embed message to insert the infos
            noble_phantasm (NoblePhantasm): Noble Phantasm Object
        """
        noble_phantasm_effect = textblob.TextBlob(noble_phantasm.effect).translate(from_lang='eng', to='pt-br')
        message_content = f'**Nome:** {noble_phantasm.name}\n**Efeito:** {noble_phantasm_effect}\n**Tipo:** {noble_phantasm.type}\n**Card:** {noble_phantasm.card}\n**Rank:** {noble_phantasm.rank}'
        discord_message.add_field(name='Fantasma Nobre', value=message_content)
    
    async def delete_servant_search(search_id: str) -> bool:
        """delete_servant_search

        Args:
            search_id (str): Id of the search who's gonna be deleted

        Returns:
            bool: Returns the status of the deletion, if succeeded or failed
        """
        search_file = FateServantController.get_searches_result_file_if_exists(search_id)
        if search_file.strip() != '' or not search_file is None:
            os.remove(search_file)
            return True
        return False
        
    @staticmethod
    def get_search_results_if_exists(search_id: str) -> tuple:
        """get_search_results_if_exists

        Get the servant search file if exists, and get it content
    
        Args:
            search_id (str): Search Id, to consult the temp files

        Returns:
            tuple: Tuple of FateGoServant objects
        """
        import jsonpickle
        result_file = FateServantController.get_searches_result_file_if_exists(search_id)
        results = None
        if result_file is not None:
            with open(result_file, 'r+') as search_result: 
                results = jsonpickle.decode(search_result.read())
        return results
            
    @staticmethod
    def get_searches_result_file_if_exists(search_id: str) -> str:
        """get_searches_result_file_if_exists

        Searches through Temporary files directory and if the search file exists, returns it
        
        Args:
            search_id (str): The Search ID it's the name of the searches results file

        Returns:
            str: directory with search_file
        """
        search_id = search_id if '.json' in search_id else '{file_name}.json'.format(file_name=search_id)
        current_servant_searches = os.listdir('./temp')
        search_result_file  = None
        for current_search in current_servant_searches:
            if Utils.check_searches_result_files(current_search, search_id):
                search_result_file = current_search
                break
        return f'./temp/{search_result_file}'
        