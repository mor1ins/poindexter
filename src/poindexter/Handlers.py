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

    pdf_generator = PdfGenerator()
    pdf_generator.process(local_dir, title)
    logger(user_id=message.user_id, log=u"Пдф сгенерирована")

    logger(user_id=message.user_id, log=u"Загружаем на сервер")
    doc = VkUploader().messages_save(local_dir % ("%s.%s" % (title, "pdf")), 'doc', message.user_id, title)

    # view_api.vk.messages.send(peer_id=message.user_id, attachment='doc%s_%s' % (doc['owner_id'], doc['id']))

    menu = MenuGenerator()
    menu.process(None, "../../out/menu.html")

    page = open("../../out/menu.html")
    text = ""
    for t in page.readlines():
        text += t

    user = vk.Session(access_token=access_token)
    user_api = vk.API(user)
    user_api.pages.save(page_id=55980612, group_id=171785116, title="Меню", text=text, v='5.85')

    url = user_api.docs.getUploadServer(group_id=171785116, v='5.85')['upload_url']
    resp = requests.post(url, files={'file': open(local_dir % ("%s.%s" % (title, "pdf")), "rb")}).json()

    doc = user_api.docs.save(file=resp['file'], title=title, v='5.85')[0]


def get_handlers():
    return handlers
