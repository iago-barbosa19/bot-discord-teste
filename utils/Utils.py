from typing import Literal
import os

class Utils:
    
    @staticmethod
    def get_emojis() -> tuple:
        dir_separator = os.path.sep
        emojis = tuple(emoji.split('.')[0] for emoji in os.listdir(f'.{dir_separator}public{dir_separator}emojis'))
        return emojis 
    
    @staticmethod
    def get_control_emojis() -> tuple:
        dir_separator = os.path.sep
        emojis = tuple(emoji.split('.')[0] for emoji in os.listdir(f'.{dir_separator}public{dir_separator}emojis{dir_separator}control'))
        return emojis   
    
    @staticmethod
    def check_searches_result_files(file_name: str, search_id: dict) -> Literal['str', 'None']:
        if file_name == search_id:
            return file_name
        return None