from abc import abstractmethod, abstractproperty, ABCMeta


class IUploader:
    __metaclass__ = ABCMeta

    @abstractmethod
    def upload(self, source, destination):
        """генерация"""
