#! /usr/bin/env python
# -*- coding: utf-8 -*-

import vk_api
import requests
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll


class VkApi:
    def __init__(self, token):
        self.vk = 0
        self.vk_session = 0
        self.session = 0
        self.upload = 0
        self.long_poll = 0
        self.event = 0
        self.token = token

    def __call__(self, *args, **kwargs):
        return self

    def vk_auth(self):

        self.vk_session = vk_api.VkApi(token=self.token)
        self.vk = self.vk_session.get_api()
        self.session = requests.session()
        self.upload = VkUpload(self.vk_session)
        self.long_poll = VkLongPoll(self.vk_session)
