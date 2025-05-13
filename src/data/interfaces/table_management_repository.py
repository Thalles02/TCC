from abc import ABC, abstractmethod
from typing import List


class TableManagementRepositoryInterface(ABC):

    @abstractmethod
    def list_keys(self, token: str) -> List[str]: pass

    @abstractmethod
    def add_column(self, token: str, column_definition: dict) -> None: pass

    @abstractmethod
    def insert_record(self, token: str, record: dict) -> None: pass

    @abstractmethod
    def edit_record(self, token: str, record: dict,
                    record_id: int) -> None: pass

    @abstractmethod
    def delete_record(self, token: str, record_id: int) -> None: pass

    @abstractmethod
    def list_records(self, token: str, filter: dict) -> List[dict]: pass

    @abstractmethod
    def list_specific_record(
        self, token: str, record_id: int) -> List[dict]: pass
