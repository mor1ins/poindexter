#! /usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
from CommandSet import BotCommandSet


def start(message, vk):
    vk.messages.send(user_id=message.user_id, message=u"Повеливайте, господин!")


def random_habrahabr(message, vk):
    vk.messages.send(user_id=message.user_id, message=u'https://habrahabr.ru/post/' + str(randint(100, 200000)) + u'/')


bot_commands = BotCommandSet()
bot_commands.add([u"Погнали", u"погнали", u"лол", u"Лол"], start)
bot_commands.add([u"Хабрахабр", ], random_habrahabr)