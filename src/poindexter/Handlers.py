#! /usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import os
import random
from Generators.PdfGenerator import PdfGenerator
from Loaders.VkLoader import VkUploader, VkLoader
import re
from Note import Note
from dependency import handlers, group_api, work_dir, logger, global_db, page_id, group_id, download_queue


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
    download_queue.queue.clear()
    download_queue.count_docs = 0


@handlers.message_handler([u"Готово"])
def vk_ready(message):
    if download_queue.count_docs > 0:
        response = group_api.vk.messages.getHistoryAttachments(
            peer_id=message.user_id, media_type=u"doc",
            count=download_queue.count_docs, start_from=0
        )
        for i in range(0, download_queue.count_docs):
            title = response['items'][i]['attachment']['doc']['title'].split('.')[0]
            ext = response['items'][i]['attachment']['doc']['ext']
            url = response['items'][i]['attachment']['doc']['url']

            download_queue.append(
                (title, ext, url)
            )
    group_api.vk.messages.send(
        user_id=message.user_id,
        message=u"Документов добавлено в очередь: %d " % download_queue.count_docs
    )


@handlers.message_handler([u"Начать"])
def vk_ready_download_handler(message):
    rand, local_dir = None, None

    if len(download_queue.queue) > 0:
        try:
            rand, local_dir = gen_random_dir()

            for i in range(0, download_queue.count_docs):
                doc_file = download_queue.queue[i]

                group_api.vk.messages.send(user_id=message.user_id, message=u"Погнали!")

                title, ext = VkLoader(message).process(doc_file, local_dir)

                PdfGenerator().process(local_dir, title)

                global_db.insert_into(Note.from_list(title, rand).__str__())

                file_for_upload = local_dir % ("%s.%s" % ("note_pdf", "pdf"))
                uploader = VkUploader(page_id=page_id, group_id=group_id, menu_title="Меню", doc_title=title,
                                      rand_id=rand)

                if uploader.upload(file_for_upload):
                    logger(user_id=message.user_id, log=u"Конспект успешно добавлен")
        except:
            logger(user_id=message.user_id, log=u"Что-то пошло не так")
        finally:
            if os.path.exists(local_dir[:-3]):
                shutil.rmtree(local_dir[:-3])
    else:
        group_api.vk.messages.send(user_id=message.user_id, message=u"Нечего грузить")


def get_handlers():
    return handlers
