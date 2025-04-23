from typing import List
from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.db.entities.workspace import Workspace as WorkspaceEntity
from src.data.interfaces.workspace_repository import WorkspaceRepositoryInterface
from src.domain.models.workspace import Workspace


class WorkspaceRepository(WorkspaceRepositoryInterface):

    @classmethod
    def insert_workspace(cls, name) -> None:
        with DBConnectionHandler() as database:
            try:
                new_registry = WorkspaceEntity(
                    name=name
                )
                database.session.add(new_registry)
                database.session.commit()
            except Exception as exception:
                database.session.rollback()
                raise exception

    @classmethod
    def list_workspaces(cls) -> List[Workspace]:
        with DBConnectionHandler() as database:
            try:
                workspaces = (
                    database.session
                    .query(WorkspaceEntity)
                    .all()
                )
                return workspaces
            except Exception as exception:
                database.session.rollback()
                raise exception
