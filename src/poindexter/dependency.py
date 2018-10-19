from APIs.DBApi import NotesDB, DB_NOTES_PATH, TABLE_NAME
from APIs.VkApi import VkApi
from credentials import vk_token, access_token, vk_login, vk_pass, app_id
from CommandSet import BotCommandSet

work_dir = '../../out/%s'
view_api = VkApi(token=vk_token)
admin_api = VkApi(token=access_token)
admin_api.vk_auth()
handlers = BotCommandSet()


class Logger:
    def __init__(self):
        self.__api = view_api

    def __call__(self, user_id, log):
        self.__api.vk.messages.send(user_id=user_id, message=log)


logger = Logger()
global_db = NotesDB("../../%s.db" % TABLE_NAME, TABLE_NAME)
global_db.remove_table()
global_db.create_table()
