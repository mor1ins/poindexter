#! /usr/bin/env python
# -*- coding: utf-8 -*-

from vk_api.longpoll import VkEventType
import dependency
import Handlers


class VKBot(object):
    def __init__(self):
        self.__commands = Handlers.get_handlers()
        self.__api = dependency.group_api

    @property
    def api(self):
        return self.__api.vk

    def auth(self):
        self.__api.vk_auth()

    def run(self):
        for event in self.__api.long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                print("start execute", event.text)

                count_docs = int(len(event.attachments) / 2)
                if count_docs > 0:
                    for i in range(1, count_docs + 1):
                        dependency.download_queue.append(
                            (event.attachments['attach%d' % i], event.attachments['attach%d_type' % i])
                        )

                self.__commands.exec_handler(event)
                print("stop execute", event.text)
