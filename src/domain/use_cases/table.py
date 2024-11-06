from abc import ABC, abstractmethod
from typing import Dict

# CRUD das Tabelas
class TableRegister(ABC):
    @abstractmethod
    def register(self, token: str, name: str) -> Dict: pass


