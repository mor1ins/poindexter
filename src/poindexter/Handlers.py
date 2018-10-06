#! /usr/bin/env python
# -*- coding: utf-8 -*-

from os import listdir
from PIL import Image
from os.path import isfile, join
from zipfile import ZipFile
from CommandSet import BotCommandSet
from Abstructions.Bot import IExecutor
from urllib import request
import requests
from fpdf import FPDF

dest_directory = '/home/morins/Projects/poindexter/out/%s'


class HandlerOwner(IExecutor):
    def __init__(self):
        super().__init__()
        # self.append()

    @staticmethod
    def start_handler(message, vk):
        vk.messages.send(user_id=message.user_id, message=u"Повеливайте, господин!")

    @staticmethod
    def vk_start_download_handler(message, vk):
        vk.messages.send(user_id=message.user_id, message=u"Жду архив (отправьте его, а потом отправьте ОК)")

    def vk_ready_download_handler(self, message, vk):
        response = vk.messages.getHistoryAttachments(peer_id=message.user_id, media_type=u"doc", count=1)

        title = response['items'][0]['attachment']['doc']['title'].split('.')[0]
        source = response['items'][0]['attachment']['doc']['url']
        ext = response['items'][0]['attachment']['doc']['ext']

        dest_for_archive = dest_directory % (title + "." + ext)
        request.urlretrieve(source, dest_for_archive)

        archive_file = ZipFile(dest_for_archive)
        archive_file.extractall(dest_directory % title)
        archive_file.close()

        photos = [dest_directory % (title + "/" + f)
                  for f in listdir(dest_directory % title)
                  if isfile(join(dest_directory % title, f))]

        pdf = FPDF()
        for image in photos:
            pdf.add_page()
            file = Image.open(image)
            box = file.getbbox()
            pdf.image(image, x=box[0], y=box[1], w=pdf.w, h=pdf.h)
        pdf.output(dest_directory % (title + ".pdf"), "F")

        upload_url = vk.docs.getMessagesUploadServer(type='doc', peer_id=message.user_id)['upload_url']
        resp = requests.post(upload_url, files={'file': open(dest_directory % (title + ".pdf"), "rb")}).json()['file']

        doc = vk.docs.save(file=resp, title='конспект')[0]

        vk.messages.send(peer_id=message.user_id, attachment='doc%s_%s' % (doc['owner_id'], doc['id']))

        self.run(dest_for_archive, dest_directory % title)

    @staticmethod
    def execute_handler(self, message, vk):
        self.run()


handlers = HandlerOwner()
bot_commands = BotCommandSet()
bot_commands.add([u"Погнали", u"погнали", u"лол", u"Лол"], handlers.start_handler)
bot_commands.add([u"Загрузить с вк"], handlers.vk_start_download_handler)
bot_commands.add([u"Ок", u'ОК', u"ок"], handlers.vk_ready_download_handler)
