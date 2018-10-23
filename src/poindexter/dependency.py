from APIs.DBApi import NotesDB, DB_NOTES_PATH, TABLE_NAME
from APIs.VkApi import VkApi
from credentials import vk_token, access_token, vk_login, vk_pass, app_id
from CommandSet import BotCommandSet
import vk
from log import *


work_dir = '../../out/%s'
group_api = VkApi(token=vk_token)

page_id = 55980612
group_id = 171785116

user = vk.Session(access_token=access_token)
user_api = vk.API(user)

handlers = BotCommandSet()

download_queue = []

logger = Logger(group_api)

global_db = NotesDB("../../%s.db" % TABLE_NAME, TABLE_NAME)
global_db.remove_table()
global_db.create_table()
