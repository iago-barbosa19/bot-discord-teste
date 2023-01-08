import redis, json
from utils import Log
from typing import Literal

class RedisDatabase:
    
    _instance = None

    def __init__(self: object, *, database_host: str, database_port: int, database_password:str) -> None: 
        self.__database_host: str = database_host
        self.__database_port: str = database_port
        self.__database_password: str = database_password
        self.__log = Log.get_logger()
    
    def __connect(self: object) -> Literal['database_connection']:
        try:
            return redis.Redis(self.__database_host, self.__database_port, password=self.__database_password)
        except Exception as ex:
            self.__log.error('Error connecting to database.', ex)
            
    def __disconnect(self: object, redis_database) -> None:
        try:
            redis_database.connection_pool.disconnect()
        except Exception as ex:
            self.__log.error('Error disconnecting to database.', ex)
    
    def set_data(self: object, key, value) -> None:
        db_connection = None
        try:
            db_connection = self.__connect()
            db_connection.set(key, value)
        except Exception as ex:
            self.__log.error('Error setting data to database.', ex)
            return
        self.__disconnect(db_connection)

    def append_to_list(self: object, key: str, values: Literal['list', 'tuple', 'str', 'int']) -> None:
        db_connection = None
        try:
            db_connection = self.__connect()
            db_connection.rpush(key, values)
        except Exception as ex:
            self.__log.error('Erro appending data to list in database.', ex)
            return
        self.__disconnect(db_connection)
        
    def get_data(self: object, key: str) -> Literal['None', 'query_data']:
        db_connection = self.__connect()
        try:
            data_acquired = db_connection.get(key)
            self.__disconnect(db_connection)
            return data_acquired.decode('utf-8')
        except Exception as ex:
            self.__log.error('Error getting data of database.', ex)
    
    def get_data_list(self:object, key_pattern: str) -> tuple:
        db_connection = self.__connect()
        try:
            keys = db_connection.keys(pattern=key_pattern)
            data_to_return = {}
            for key in keys:
                data_to_return[key.decode('utf-8')] = db_connection.get(key).decode('utf-8')
            self.__disconnect(db_connection)
            return data_to_return
        except Exception as ex:
            self.__log.error('Error getting hash data list of database.', ex)

    def delete_data(self: object, key_pattern: str) -> None:
        db_connection = self.__connect()
        try:
            db_connection.delete(key_pattern)
            self.__disconnect(db_connection)
        except Exception as ex:
            self.__log.error('Error deleting data of database.', ex)
    
    @classmethod
    def get_database(database: object) -> object:
        if database._instance is None:
            data = None
            with open('appsettings.json', 'r') as configs:
                data = json.load(configs)['database_configuration']
            database._instance = database( database_host = data['database_host'],
                                            database_port = data['port'],
                                            database_password = data['database_login']['password'])
        return database._instance