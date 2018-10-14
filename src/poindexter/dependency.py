from APIs.DBApi import NotesDB, DB_NOTES_PATH, TABLE_NAME
from APIs.VkApi import VkApi
from credentials import vk_token
from CommandSet import BotCommandSet


work_dir = '../../out/%s'
view_api = VkApi(vk_token)
handlers = BotCommandSet()


global_db = NotesDB(DB_NOTES_PATH, TABLE_NAME)
