#! /usr/bin/env python
# -*- coding: utf-8 -*-

from vk_api.longpoll import VkEventType
import dependency
import Handlers


class VKBot(object):
    def __init__(self):
        self.__commands = Handlers.get_handlers()
        self.__api = dependency.view_api

    @property
    def api(self):
        return self.__api.vk

    def auth(self):
        self.__api.vk_auth()

    def run(self):
        for event in self.__api.long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                print("start execute", event.text)
                self.__commands.exec_handler(event)
                print("stop execute", event.text)

