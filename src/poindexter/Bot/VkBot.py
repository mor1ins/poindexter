#! /usr/bin/env python
# -*- coding: utf-8 -*-

from vk_api.longpoll import VkEventType
from credentials import vk_token
from APIs.VkApi import VkApi
from CommandSet import BotCommandSet


class VKBot(object):
    def __init__(self):
        self.commands = BotCommandSet()
        self.vk = VkApi(vk_token)

    def __call__(self, *args, **kwargs):
        return self

    @property
    def api(self):
        return self.vk.vk

    def auth(self):
        self.vk.vk_auth()

    def message_handler(self, commands):
        def decorator(f):
            self.commands.add(commands, f)
            return f
        return decorator

    def run(self):
        for event in self.vk.long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                print("start execute", event.text)
                self.commands.exec_handler(event)
                print("stop execute", event.text)

