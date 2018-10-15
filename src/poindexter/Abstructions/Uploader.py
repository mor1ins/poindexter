#! /usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod, ABCMeta


class IUploader(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def upload(self, source, destination):
        """генерация"""

    def save_doc(self, *arg, **keywords):
        """сохранение документа на сервере сервиса"""
