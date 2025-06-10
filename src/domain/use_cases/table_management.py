from abc import ABC, abstractmethod
from typing import Dict, List, Tuple


class TableManagementListKeys(ABC):
    @abstractmethod
    def list_keys(self, token: str) -> List[Tuple[str, str]]: pass


class TableManagementAddColumn(ABC):
    @abstractmethod
    def add_column(self, token: str, column_definition: dict) -> Dict: pass


class TableManagementInsertRecord(ABC):
    @abstractmethod
    def insert_record(self, token: str, record: dict) -> None: pass


class TableManagementEditRecord(ABC):
    @abstractmethod
    def edit_record(self, token: str, record: dict,
                    record_id: int) -> None: pass


class TableManagementDeleteRecord(ABC):
    @abstractmethod
    def delete_record(self, token: str, record_id: int) -> None: pass


class TableManagementListRecords(ABC):
    @abstractmethod
    def list_records(self, token: str, filter: dict) -> List[dict]: pass


class TableManagementListSpecificRecord(ABC):
    @abstractmethod
    def list_specific_record(
        self, token: str, record_id: int) -> List[dict]: pass
