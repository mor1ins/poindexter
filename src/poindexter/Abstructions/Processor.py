from abc import abstractmethod, abstractproperty, ABCMeta


class IProcessor:
    __metaclass__ = ABCMeta

    @abstractmethod
    def process(self, source, destination):
        """обработка"""
