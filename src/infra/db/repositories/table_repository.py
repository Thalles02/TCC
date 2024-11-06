from typing import List
from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.db.entities.table import Table as TableEntity
from src.data.interfaces.table_repository import TableRepositoryInterface
from src.domain.models.table import Table


class TableRepository(TableRepositoryInterface):

    @classmethod
    def insert_table(cls, token: str, name: str) -> None:
        with DBConnectionHandler() as database:
            try:
                new_registry = TableEntity(
                    token=token,
                    name=name
                )
                database.session.add(new_registry)
                database.session.commit()
            except Exception as exception:
                database.session.rollback()
                raise exception

    @classmethod
    def list_tables(cls) -> List[Table]:
        with DBConnectionHandler() as database:
            try:
                tables = (
                    database.session
                    .query(TableEntity)
                    .all()
                )
                return tables
            except Exception as exception:
                database.session.rollback()
                raise exception
