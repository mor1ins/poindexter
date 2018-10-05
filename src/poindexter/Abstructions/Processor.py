#! /usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod, abstractproperty, ABCMeta


class IProcessor:
    __metaclass__ = ABCMeta

    @abstractmethod
    def process(self, source, destination):
        """обработка"""

    @abstractmethod
    def commit(self):
        """подтверждение изменений"""

    @abstractmethod
    def rollback(self):
        """откат изменений"""

