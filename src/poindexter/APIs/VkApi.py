#! /usr/bin/env python
# -*- coding: utf-8 -*-

import vk_api
import requests
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll
from Abstructions.Uploader import IUploader


class VkApi:
    def __init__(self, login: str=None, passwd: str=None, token: str=None):
        self.vk = 0
        self.vk_session = 0
        self.session = 0
        self.upload = 0
        self.long_poll = 0
        self.event = 0
        self.login = login
        self.passwd = passwd
        self.token = token

    def vk_auth(self):
        if self.token is not None:
            self.vk_session = vk_api.VkApi(token=self.token)
        else:
            self.vk_session = vk_api.VkApi(login=self.login, password=self.passwd)
            self.vk_session.auth()

        self.vk = self.vk_session.get_api()
        self.session = requests.session()
        self.upload = VkUpload(self.vk_session)
        self.long_poll = VkLongPoll(self.vk_session)
