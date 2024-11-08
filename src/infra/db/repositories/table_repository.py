from typing import List
from sqlalchemy import text
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

                # Executar o SQL para criar a tabela dinâmica de dados
                with database.get_engine().connect() as connection:
                    connection = connection.execution_options(
                        isolation_level="AUTOCOMMIT")
                    sql = text("""
                        CREATE TABLE {token_str} (
                            id_{token_str} serial PRIMARY KEY,
                            criado_por integer,
                            criado_em timestamp NOT NULL DEFAULT now(),
                            atualizado_por integer,
                            atualizado_em timestamp NOT NULL DEFAULT now(),
                            FOREIGN KEY (criado_por) REFERENCES users(id) ON DELETE SET DEFAULT,
                            FOREIGN KEY (atualizado_por) REFERENCES users(id) ON DELETE SET DEFAULT
                        );
                    """.format(token_str=token))
                    connection.execute(sql)
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
