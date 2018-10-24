from APIs.DBApi import NotesDB, DB_NOTES_PATH, TABLE_NAME
from APIs.VkApi import VkApi
from credentials import vk_token, access_token, vk_login, vk_pass, app_id
from CommandSet import BotCommandSet
import vk
from log import *


class DownloadQueue:
    def __init__(self):
        self.count_docs = 0
        self.queue = []

    def append(self, elem):
        self.queue.append(elem)

    def inc(self, count):
        self.count_docs += count

    def clear(self):
        self.queue.clear()
        self.count_docs = 0


work_dir = '../../out/%s'
group_api = VkApi(token=vk_token)

page_id = 55980612
group_id = 171785116

user = vk.Session(access_token=access_token)
user_api = vk.API(user)

download_queue = DownloadQueue()

handlers = BotCommandSet()

logger = Logger(group_api)

global_db = NotesDB("../../%s.db" % TABLE_NAME, TABLE_NAME)
global_db.remove_table()
global_db.create_table()
