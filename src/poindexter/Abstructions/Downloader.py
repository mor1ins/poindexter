#! /usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod, abstractproperty, ABCMeta
from Abstructions.Processor import IProcessor


class IDownloader(IProcessor):
    __metaclass__ = ABCMeta

    @abstractmethod
    def download(self, source, destination):
        """скачать"""

    def process(self, source, destination):
        return self.download(source, destination)

