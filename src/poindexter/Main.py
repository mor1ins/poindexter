#! /usr/bin/env python
# -*- coding: utf-8 -*-

import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
from random import randint


vk_token = "abf8b194c2bf48f1578ae829b95d808fee50199d6f8f07a4c9a79591832fcd5900fce1293d54a8e40d1a1"


class VKBot:
    vk = 0
    vk_session = 0
    session = 0
    upload = 0
    long_poll = 0
    event = 0

    def __init__(self, log=None, passwd=None, token=None):
        if vk_token:
            self.vk_session = vk_api.VkApi(token=vk_token)
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

    def __command_handler__(self, commands, handler):
        message_set = self.event.text.split(u' ')
        for command in commands:
            if command in message_set:
                handler(self.event, self.vk)
                break

    def __query_manager__(self, queryset):
        for item in queryset:
            self.__command_handler__(item[0], item[1])

    def run(self, query):
        for event in self.long_poll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self.event = event
                self.__query_manager__(query)


def start(message, vk):
    vk.messages.send(user_id=message.user_id, message=u"Повеливайте")


def random_habrahabr(message, vk):
    vk.messages.send(user_id=message.user_id, message=u'https://habrahabr.ru/post/' + str(randint(100, 200000)) + u'/')


if __name__ == '__main__':
    queryset = [[[u"Погнали", u"погнали", u"лол", u"Лол"], start], [[u"Хабрахабр", ], random_habrahabr]]
    # if you want use bot by community token
    bot = VKBot(vk_token)
    # if you want use bot by your account
    # bot = VKBot(log='your_login', passwd='your_passwd')
    bot.run(query=queryset)
