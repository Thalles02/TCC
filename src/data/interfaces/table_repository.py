from abc import ABC, abstractmethod
from typing import List
from src.domain.models.table import Table


class TableRepositoryInterface(ABC):
    @abstractmethod
    def insert_table(self, token: str, name: str) -> None: pass

    @abstractmethod
    def list_tables(self) -> List[Table]: pass
