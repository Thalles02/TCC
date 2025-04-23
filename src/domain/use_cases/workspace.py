from abc import ABC, abstractmethod
from typing import Dict


class WorkspaceRegister(ABC):
    @abstractmethod
    def register(self, name: str) -> Dict: pass


class WorkspaceList(ABC):
    @abstractmethod
    def list_workspaces(self) -> Dict: pass


class WorkspaceAddTable(ABC):
    @abstractmethod
    def add_table(self, id_workspace: int, token_table: str) -> Dict: pass
