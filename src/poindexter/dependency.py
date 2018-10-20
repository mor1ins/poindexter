from APIs.DBApi import NotesDB, DB_NOTES_PATH, TABLE_NAME
from APIs.VkApi import VkApi
from credentials import vk_token, access_token, vk_login, vk_pass, app_id
from CommandSet import BotCommandSet
import vk

class Logger:
    def __init__(self):
        self.__api = group_api

    def __call__(self, user_id, log):
        self.__api.vk.messages.send(user_id=user_id, message=log)
        print(log)


work_dir = '../../out/%s'
group_api = VkApi(token=vk_token)

user = vk.Session(access_token=access_token)
user_api = vk.API(user)

handlers = BotCommandSet()

logger = Logger()

global_db = NotesDB("../../%s.db" % TABLE_NAME, TABLE_NAME)
global_db.remove_table()
global_db.create_table()
