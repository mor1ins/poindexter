#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
from zipfile import ZipFile

from Generators.PdfGenerator import PdfGenerator
from Loaders.VkLoader import VkUploader, VkLoader
from dependency import handlers, view_api, work_dir, logger


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

    view_api.vk.messages.send(peer_id=message.user_id, attachment='doc%s_%s' % (doc['owner_id'], doc['id']))


def get_handlers():
    return handlers
