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
        self._downloaders = []
        self._processors = []
        self._generators = []
        self._uploaders = []
        self._error_handler = []

        self._order = []

    def get(self, typename):
        if issubclass(typename, IDownloader):
            return self._downloaders
        elif issubclass(typename, IGenerator):
            return self._generators
        elif issubclass(typename, IProcessor):
            return self._processors
        elif issubclass(typename, IUploader):
            return self._uploaders
        else:
            return self._error_handler

    def append(self, obj):
        self.get(type(obj)).append(obj)
        self._order.append(obj)

    def run(self, source, destination):
        for processor in self._order:
            processor.process(source, destination)
