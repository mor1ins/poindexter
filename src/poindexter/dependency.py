from APIs.DBApi import NotesDB, DB_NOTES_PATH, TABLE_NAME
from APIs.VkApi import VkApi
from credentials import vk_token
from CommandSet import BotCommandSet

work_dir = '../../out/%s'
view_api = VkApi(vk_token)
handlers = BotCommandSet()


class Logger:
    def __init__(self):
        self.__api = view_api

    def __call__(self, user_id, log):
        self.__api.vk.messages.send(user_id=user_id, message=log)


logger = Logger()
global_db = NotesDB(DB_NOTES_PATH, TABLE_NAME)
