#! /usr/bin/env python
# -*- coding: utf-8 -*-

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


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

