#! /usr/bin/env python
# -*- coding: utf-8 -*-

import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
from random import randint
from credentials import vk_token


class SingletonDecorator:
    def __init__(self, klass):
        self.klass = klass
        self.instance = None

    def __call__(self, *args, **kwds):
        if self.instance is None:
            self.instance = self.klass(*args, **kwds)
        return self.instance


class BotCommand:
    def __init__(self, names, handler):
        self.__names = set()
        for name in names:
            self.__names.add(name)
        self.__handler = handler

    def __call__(self, *args, **kwargs):
        if self.__handler is not None:
            self.__handler(*args, **kwargs)

    def __eq__(self, other):
        if type(other) == vk_api.longpoll.Event:
            return self.__names.__contains__(other.text)
        elif type(other) == BotCommand:
            return self.__names.intersection(other.__names).__len__() > 0
        return False

    def __hash__(self):
        return hash(self.__names.__hash__)


class BotCommandSet:
    def __init__(self):
        self.__queryset = set()

    def __find__(self, command):
        for cmd in self.__queryset:
            if cmd == command:
                return cmd
        return None

    def add(self, command, handler):
        cmd = BotCommand(command, handler)
        self.__queryset.add(cmd)

    def __call__(self, event, *args, **kwargs):
        cmd = self.__find__(event)
        return cmd(event, *args, **kwargs)


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


def start(message, vk):
    vk.messages.send(user_id=message.user_id, message=u"Повеливайте, господин!")


def random_habrahabr(message, vk):
    vk.messages.send(user_id=message.user_id, message=u'https://habrahabr.ru/post/' + str(randint(100, 200000)) + u'/')


if __name__ == '__main__':
    bot_commands = BotCommandSet()
    bot_commands.add([u"Погнали", u"погнали", u"лол", u"Лол"], start)
    bot_commands.add([u"Хабрахабр", ], random_habrahabr)
    # if you want use bot by community token
    bot = VKBot(token=vk_token, commands=bot_commands)
    # if you want use bot by your account
    # bot = VKBot(log='your_login', passwd='your_passwd')
    bot.run()
