from abc import abstractmethod, abstractproperty, ABCMeta
from Abstructions.Processor import IProcessor


class IUploader(IProcessor):

    @abstractmethod
    def upload(self, source, destination):
        """генерация"""

    def process(self, source, destination):
        return self.upload(source, destination)
