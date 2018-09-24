from abc import abstractmethod, abstractproperty, ABCMeta


class IDownloader:
    __metaclass__ = ABCMeta

    @abstractmethod
    def download(self, source, destination):
        """скачать"""
