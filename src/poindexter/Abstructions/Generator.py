from abc import abstractmethod, abstractproperty, ABCMeta


class IGenerator:
    __metaclass__ = ABCMeta

    @abstractmethod
    def generate(self, source, destination):
        """генерация"""
