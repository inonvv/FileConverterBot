from abc import ABC, abstractmethod


class File(ABC):
    @property
    @abstractmethod
    def extension(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass
