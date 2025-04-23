# pylint: disable=broad-exception-raised
from typing import Dict, List
from src.domain.use_cases.workspace import WorkspaceRegister as WorkspaceRegisterInterface
from src.domain.use_cases.workspace import WorkspaceList as WorkspaceListInterface
from src.data.interfaces.table_repository import TableRepositoryInterface
from src.data.interfaces.workspace_repository import WorkspaceRepositoryInterface
from src.domain.models.workspace import Workspace
from src.errors.types import HttpNotFoundError, HttpBadRequestError


class WorkspaceRegister(WorkspaceRegisterInterface):
    def __init__(self, workspace_repository: WorkspaceRepositoryInterface) -> None:
        self.__workspace_repository = workspace_repository

    def register(self, name: str) -> Dict:

        self.__registry_workspace(name)
        response = self.__format_response(name)
        return response


    def __registry_workspace(self, name: str) -> None:
        self.__workspace_repository.insert_workspace(name)

    @classmethod
    def __format_response(cls, name: str) -> Dict:
        response = {
            "type": "Workspace",
            "count": 1,
            "attributes": {
                "name": name
            }
        }
        return response


class WorkspaceList(WorkspaceListInterface):
    def __init__(self, workspace_repository: WorkspaceRepositoryInterface) -> None:
        self.__workspace_repository = workspace_repository

    def list_workspaces(self) -> Dict:
        workspaces = self.__search_workspace()
        response = self.__format_response(workspaces)
        return response

    def __search_workspace(self) -> List[Workspace]:
        workspace = self.__workspace_repository.list_workspaces()
        if workspace == []:
            raise HttpNotFoundError('Nenhuma Tabela encontrada')
        return workspace

    @classmethod
    def __format_response(cls, workspaces: List[Workspace]) -> Dict:
        attributes = []
        for item in workspaces:
            attributes.append(
                {"id": item.id_workspace, "name": item.name}
            )

        response = {
            "type": "Workspaces",
            "count": len(workspaces),
            "attributes": attributes
        }

        return response
