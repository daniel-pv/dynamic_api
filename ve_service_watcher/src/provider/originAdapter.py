
from abc import ABC, abstractmethod
from entities.endpoint import ApiFile


class OriginAdapter(ABC):

    def __init__(self, source_path, source_name):
        self.source_path = source_path
        self.source_name = source_name

    @abstractmethod
    def read(self, source: str) -> ApiFile:
        pass
