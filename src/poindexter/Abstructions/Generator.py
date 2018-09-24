from abc import abstractmethod, abstractproperty, ABCMeta
from Abstructions.Processor import IProcessor


class IGenerator(IProcessor):
    @abstractmethod
    def generate(self, source, destination):
        """генерация"""

    def process(self, source, destination):
        return self.generate(source, destination)
