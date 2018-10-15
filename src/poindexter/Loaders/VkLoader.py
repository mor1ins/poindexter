#! /usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABC
from zipfile import ZipFile

from Abstructions.Downloader import IDownloader
from Abstructions.Uploader import IUploader
import dependency
import requests
from urllib import request
import random
import os


class VkLoader(IDownloader):
    def __init__(self):
        self.__api = dependency.view_api
        self.__log = dependency.logger

    def download(self, source, destination):
        response = self.__api.vk.messages.getHistoryAttachments(peer_id=source, media_type=u"doc", count=1)

        title = response['items'][0]['attachment']['doc']['title'].split('.')[0]
        ext = response['items'][0]['attachment']['doc']['ext']
        url = response['items'][0]['attachment']['doc']['url']

        if ext != "zip":
            self.__log(user_id=source, log=u"Неправильный формат файла")
            return

        download_destination = destination % ("%s.%s" % (title, ext))
        request.urlretrieve(url, download_destination)
        self.__log(user_id=source, log=u"Файл скачали")

        only_archive = [item for item
                        in os.listdir(destination[:-3])
                        if item.split('.')[1] == "zip"][0]

        title = only_archive.split('.')[0]
        ext = only_archive.split('.')[1]

        archive_file = ZipFile(destination % only_archive)
        archive_file.extractall(destination % title)
        archive_file.close()

        return title, ext


class VkUploader(IUploader, ABC):
    def __init__(self):
        self.__api = dependency.view_api

    def messages_save(self, destination, type, user_id, file_name):
        upload_url = self.__api.vk.docs.getMessagesUploadServer(type=type, peer_id=user_id)['upload_url']
        resp = requests.post(upload_url, files={'file': open(destination, "rb")}).json()
        doc = self.__api.vk.docs.save(file=resp['file'], title=file_name)[0]
        return doc
