#! /usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import os
import random
from Generators.PdfGenerator import PdfGenerator
from Loaders.VkLoader import VkUploader, VkLoader
import re
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from Note import Note
from dependency import handlers, group_api, user_api, work_dir, logger, global_db, page_id, group_id, download_queue
from strings import *


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


@handlers.message_handler([BTN_PS_DL])
def webdav_start_download_handler(message):
    group_api.vk.messages.send(user_id=message.user_id, message=LOG_START_PS_DL)


@handlers.message_handler([BTN_END_SESSION])
def end_session(message):
    keyboard = VkKeyboard()
    keyboard.add_button(BTN_START_SESSION, color=VkKeyboardColor.PRIMARY)
    group_api.vk.messages.send(user_id=message.user_id, message=LOG_END_SESSION,
                               keyboard=keyboard.get_keyboard())


@handlers.message_handler([BTN_START_SESSION])
def start_handler(message):
    keyboard = VkKeyboard()

    group_api.vk.messages.send(user_id=message.user_id, message=LOG_BEGIN_MESSAGE,
                               keyboard=keyboard.get_empty_keyboard())

    response = user_api.groups.getMembers(
        group_id=group_id, sort='time_desc',
        filter='managers', v='5.87'
    )
    admins = [member['id'] for member in response['items']]

    if message.user_id in admins:
        download_queue.clear()
        keyboard.add_button(BTN_VK_DL, color=VkKeyboardColor.PRIMARY)
        keyboard.add_button(BTN_PS_DL, color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(BTN_ADD, color=VkKeyboardColor.POSITIVE)
        keyboard.add_button(BTN_READY, color=VkKeyboardColor.NEGATIVE)
        keyboard.add_line()
        keyboard.add_button(BTN_END_SESSION, color=VkKeyboardColor.DEFAULT)
        group_api.vk.messages.send(user_id=message.user_id, message=LOG_LVL_ADMIN,
                                   keyboard=keyboard.get_keyboard())
    else:
        group_api.vk.messages.send(user_id=message.user_id, message=LOG_NO_ADMIN_MESSAGE)


@handlers.message_handler([BTN_VK_DL])
def vk_start_download_handler(message):
    group_api.vk.messages.send(user_id=message.user_id, message=LOG_START_VK_DL)
    download_queue.clear()


@handlers.message_handler([BTN_ADD])
def vk_ready(message):
    text = LOG_DOC_IN_QUEUE % download_queue.count_docs
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
            text += "%d. %s\n" % (i + 1, title)
    group_api.vk.messages.send(
        user_id=message.user_id,
        message=text
    )


@handlers.message_handler([BTN_READY])
def vk_ready_download_handler(message):
    rand, local_dir = None, None
    log_for_user = ""

    if len(download_queue.queue) > 0:
        group_api.vk.messages.send(
            user_id=message.user_id,
            message=LOG_START_DL_NOTES
        )
        for i in range(0, download_queue.count_docs):
            try:
                rand, local_dir = gen_random_dir()

                doc_file = download_queue.queue[i]

                log_for_user += u"%d. %s - " % (i + 1, doc_file[0])

                title, ext = VkLoader(message).process(doc_file, local_dir)

                PdfGenerator().process(local_dir, title)

                global_db.insert_into(Note.from_list(title, rand).__str__())

                file_for_upload = local_dir % ("%s.%s" % ("note_pdf", "pdf"))
                uploader = VkUploader(
                    page_id=page_id, group_id=group_id, menu_title="Меню",
                    doc_title=title, rand_id=rand
                )

                if uploader.upload(file_for_upload):
                    log_for_user += LOG_SUCCESS_ADD_NOTE + '\n\n'
            except Exception as err:
                log_for_user += LOG_ERROR_ADD_NOTE + "\n" + err.args[0] + '\n\n'
            finally:
                if os.path.exists(local_dir[:-3]):
                    shutil.rmtree(local_dir[:-3])

        log_for_user += LOG_END_DL_NOTES
        download_queue.clear()
        keyboard = VkKeyboard()
        keyboard.add_button(BTN_START_SESSION, color=VkKeyboardColor.PRIMARY)
        group_api.vk.messages.send(user_id=message.user_id, message=log_for_user,
                                   keyboard=keyboard.get_keyboard())
    else:
        group_api.vk.messages.send(user_id=message.user_id, message=LOG_NOTHING_FOR_DL)


def get_handlers():
    return handlers
