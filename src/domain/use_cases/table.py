from abc import ABC, abstractmethod
from typing import Dict


class TableRegister(ABC):
    @abstractmethod
    def register(self, token: str, name: str) -> Dict: pass


class TableList(ABC):
    @abstractmethod
    def list_tables(self) -> Dict: pass
