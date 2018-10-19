#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
from zipfile import ZipFile

import requests
import vk
from Generators.PdfGenerator import PdfGenerator
from Generators.MenuGenerator import MenuGenerator
from Loaders.VkLoader import VkUploader, VkLoader
import re
from Note import Note
from APIs.DBApi import format_dir
from dependency import handlers, view_api, access_token, app_id, vk_login, vk_pass, work_dir, logger, global_db, \
    admin_api


@handlers.message_handler([u"Погнали", u"погнали", u"лол", u"Лол"])
def start_handler(message):
    view_api.vk.messages.send(user_id=message.user_id, message=u"Повеливайте, господин!")


@handlers.message_handler([u"Загрузить с вк"])
def vk_start_download_handler(message):
    view_api.vk.messages.send(user_id=message.user_id, message=u"Жду архив (отправьте его, а потом отправьте ОК)")


@handlers.message_handler([u"Ок", u'ОК', u"ок"])
def vk_ready_download_handler(message):
    view_api.vk.messages.send(user_id=message.user_id, message=u"Погнали!")

    rand = random.randint(1, 9999)
    while os.path.exists(work_dir % rand):
        rand = random.randint(1, 9999)
    local_dir = work_dir % ("%d/%s" % (rand, "%s"))
    os.mkdir(local_dir[:-3])

    downloader = VkLoader()
    title, ext = downloader.process(message.user_id, local_dir)
    logger(user_id=message.user_id, log=u"Разархивировали")
    matches = re.findall(format_dir, title, re.U)
    # if len(matches) < 0:
    #     logger(user_id=message.user_id, log=u"Некорректное имя архива")
    #     return

    pdf_generator = PdfGenerator()
    pdf_generator.process(local_dir, title)
    logger(user_id=message.user_id, log=u"Пдф сгенерирована")

    # doc = VkUploader().messages_save(local_dir % ("%s.%s" % (title, "pdf")), 'doc', message.user_id, title)
    # view_api.vk.messages.send(peer_id=message.user_id, attachment='doc%s_%s' % (doc['owner_id'], doc['id']))

    global_db.insert_into(Note.fromList(matches[0]).__str__())

    menu = MenuGenerator()
    menu.process(None, "../../out/menu.html")

    page = open("../../out/menu.html")
    text = ""
    for t in page.readlines():
        text += t

    user = vk.Session(access_token=access_token)
    user_api = vk.API(user)
    user_api.pages.save(page_id=55980612, group_id=171785116, title="Меню", text=text, v='5.85')

    logger(user_id=message.user_id, log=u"Загружаем на сервер")

    url = user_api.docs.getUploadServer(group_id=171785116, v='5.85')['upload_url']
    file_for_upload = local_dir % ("%s.%s" % ("note_pdf", "pdf"))
    if os.path.exists(file_for_upload):
        # file = {title: open(file_for_upload, "rb")}
        resp = requests.post(url, files={'file': open(file_for_upload, "rb")}).json()
        doc = user_api.docs.save(file=resp['file'], title=title, v='5.85')[0]
        logger(user_id=message.user_id, log=u"Конспект успешно добавлен")
        return
    logger(user_id=message.user_id, log=u"Что-то пошло не так")


def get_handlers():
    return handlers
