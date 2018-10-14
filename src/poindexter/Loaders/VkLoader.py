#! /usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABC

from Abstructions.Downloader import IDownloader
from Abstructions.Uploader import IUploader
import dependency
import requests


class VkLoader(IDownloader):
    def download(self, source, destination):
        pass


class VkUploader(IUploader, ABC):
    def __init__(self):
        self.__api = dependency.view_api

    def messages_save(self, destination, type, user_id, file_name):
        upload_url = self.__api.vk.docs.getMessagesUploadServer(type=type, peer_id=user_id)['upload_url']
        resp = requests.post(upload_url, files={'file': open(destination, "rb")}).json()
        doc = self.__api.vk.docs.save(file=resp['file'], title=file_name)[0]
        return doc
