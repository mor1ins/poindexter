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
from Generators.MenuGenerator import MenuGenerator

class VkLoader(IDownloader):
    def __init__(self):
        self.__api = dependency.group_api
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
    def __init__(self, group_id=None, menu_title=None, doc_title=None, page_id=None, rand_id=None):
        self.__api = dependency.user_api
        self.__group_id = group_id
        self.__menu_title = menu_title
        self.__doc_title = doc_title
        self.__page_id = page_id
        self.__rand_id = rand_id
        self.db = dependency.global_db

    def page_save(self, **keys):
        MenuGenerator().process(None, "../../out/menu.html")
        text = ""
        with open("../../out/menu.html") as page:
            for t in page.readlines():
                text += t
        self.__api.pages.save(**keys, text=text, v='5.85')

    def doc_save(self, file_for_upload, ):
        url = self.__api.docs.getUploadServer(group_id=self.__group_id, v='5.85')['upload_url']
        if os.path.exists(file_for_upload):
            resp = requests.post(url, files={'file': open(file_for_upload, "rb")}).json()
            doc = self.__api.docs.save(file=resp['file'], title=self.__doc_title, v='5.85')[0]
            self.db.update_url(self.__rand_id, doc['url'])
            return True
        return False

    def upload(self, source):
        is_uploaded = self.doc_save(source)
        self.page_save(page_id=self.__page_id, group_id=self.__group_id, title="Меню")
        return is_uploaded
    # def messages_save(self, destination, type, user_id, file_name):
    #     upload_url = self.__api.vk.docs.getMessagesUploadServer(type=type, peer_id=user_id)['upload_url']
    #     resp = requests.post(upload_url, files={'file': open(destination, "rb")}).json()
    #     doc = self.__api.vk.docs.save(file=resp['file'], title=file_name)[0]
    #     return doc
