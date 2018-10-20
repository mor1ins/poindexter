#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
from Generators.PdfGenerator import PdfGenerator
from Generators.MenuGenerator import MenuGenerator
from Loaders.VkLoader import VkUploader, VkLoader
import re
from Note import Note
from APIs.DBApi import format_dir
from dependency import handlers, group_api, work_dir, logger, global_db


def gen_random_dir():
    rand = random.randint(1, 9999)
    while os.path.exists(work_dir % rand):
        rand = random.randint(1, 9999)
    local_dir = work_dir % ("%d/%s" % (rand, "%s"))
    os.mkdir(local_dir[:-3])
    return rand, local_dir


def delete_dir(local_dir: str):
    os.rmdir(local_dir)


def is_correct_name(regexp, name):
    matches = re.findall(regexp, name, re.U)
    return len(matches) < 0


@handlers.message_handler([u"Погнали", u"погнали", u"лол", u"Лол"])
def start_handler(message):
    group_api.vk.messages.send(user_id=message.user_id, message=u"Повеливайте, господин!")


@handlers.message_handler([u"Загрузить с вк"])
def vk_start_download_handler(message):
    group_api.vk.messages.send(user_id=message.user_id, message=u"Жду архив (отправьте его, а потом отправьте ОК)")


@handlers.message_handler([u"Ок", u'ОК', u"ок"])
def vk_ready_download_handler(message):
    group_api.vk.messages.send(user_id=message.user_id, message=u"Погнали!")
    rand, local_dir = gen_random_dir()
    title, ext = VkLoader().process(message.user_id, local_dir)

    if is_correct_name("zip", ext):
        logger(user_id=message.user_id, log=u"Некорректный формат архиива")
        return
    logger(user_id=message.user_id, log=u"Разархивировали")
    if is_correct_name(format_dir, title):
        logger(user_id=message.user_id, log=u"Некорректное имя архива")
        return

    PdfGenerator().process(local_dir, title)
    logger(user_id=message.user_id, log=u"Пдф сгенерирована")

    matches = re.findall(format_dir, title, re.U)
    global_db.insert_into(Note.from_list(matches[0], rand).__str__())

    logger(user_id=message.user_id, log=u"Загружаем на сервер")

    file_for_upload = local_dir % ("%s.%s" % ("note_pdf", "pdf"))
    uploader = VkUploader(page_id=55980612, group_id=171785116, menu_title="Меню", doc_title=title, rand_id=rand)
    is_uploaded = uploader.upload(file_for_upload)

    if is_uploaded:
        logger(user_id=message.user_id, log=u"Конспект успешно добавлен")
    else:
        logger(user_id=message.user_id, log=u"Что-то пошло не так")


def get_handlers():
    return handlers
