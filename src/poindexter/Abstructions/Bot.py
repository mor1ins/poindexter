#! /usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod, abstractproperty, ABCMeta
from Abstructions.Generator import IGenerator
from Abstructions.Downloader import IDownloader
from Abstructions.Processor import IProcessor
from Abstructions.Uploader import IUploader


class IExecutor:
    # __metaclass__ = ABCMeta

    def __init__(self):
        self._order = []

    def append(self, obj):
        self.get(type(obj)).append(obj)
        self._order.append(obj)

    def run(self, source, destination):
        for processor in self._order:
            processor.process(source, destination)
