from abc import ABC, abstractmethod
from typing import List
from src.domain.models.workspace import Workspace


class WorkspaceRepositoryInterface(ABC):
    @abstractmethod
    def insert_workspace(self, name: str) -> None: pass

    @abstractmethod
    def list_workspaces(self) -> List[Workspace]: pass
