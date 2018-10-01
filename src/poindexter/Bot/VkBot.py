#! /usr/bin/env python
# -*- coding: utf-8 -*-

import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
from credentials import vk_token
from CommandSet import BotCommandSet


class VKBot:
    vk = 0
    vk_session = 0
    session = 0
    upload = 0
    long_poll = 0
    event = 0
    bot_commands = BotCommandSet()

    def vk_auth(self, log=None, passwd=None, auth_token=None):
        if vk_token:
            self.vk_session = vk_api.VkApi(token=auth_token)
        else:
            self.vk_session = vk_api.VkApi(log, passwd)
            try:
                self.vk_session.auth()
            except vk_api.AuthError as error_msg:
                print(error_msg)
                return
        self.vk = self.vk_session.get_api()
        self.session = requests.session()
        self.upload = VkUpload(self.vk_session)
        self.long_poll = VkLongPoll(self.vk_session)

    def __init__(self, log=None, passwd=None, token=None, commands=None):
        self.vk_auth(log, passwd, token)
        self.bot_commands = commands

    def run(self):
        for event in self.long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self.event = event
                self.bot_commands(event, self.vk)
