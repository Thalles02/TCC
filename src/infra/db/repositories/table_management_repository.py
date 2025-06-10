
# pylint: disable=protected-access
from typing import List, Any, Tuple
from sqlalchemy import text, bindparam, column, inspect
import sqlalchemy
from src.infra.db.settings.connection import DBConnectionHandler
from src.data.interfaces.table_management_repository import TableManagementRepositoryInterface


class TableManagementRepository(TableManagementRepositoryInterface):

    @classmethod
    def add_column(cls, token: str, column_definition: dict) -> None:
        with DBConnectionHandler() as database:
            try:
                # Executar o SQL para criar a tabela dinâmica de dados
                with database.get_engine().connect() as connection:
                    connection = connection.execution_options(
                        isolation_level="AUTOCOMMIT")

                    sql = text("""
                        ALTER TABLE {token_str} ADD COLUMN {column_name} {column_type};
                    """.format(token_str=token, column_name=column_definition['column_name'], column_type=column_definition['column_type']))

                    connection.execute(sql)
            except Exception as exception:
                database.session.rollback()
                raise exception

    @classmethod
    def insert_record(cls, token: str, record: dict) -> None:
        with DBConnectionHandler() as database:
            try:
                # Extrair as chaves e valores do dicionário
                columns = ', '.join(record.keys())
                values = ', '.join([f":{key}" for key in record.keys()])

                # Executar o SQL para inserir dados na tabela dinâmica
                with database.get_engine().connect() as connection:

                    connection = connection.execution_options(
                        isolation_level="AUTOCOMMIT")

                    sql = text("""INSERT INTO {} ({}) VALUES ({});""".format(
                        token, columns, values))

                    print(list(record.values()))

                    print(record)

                    connection.execute(sql, record)
            except Exception as exception:
                database.session.rollback()
                raise exception

    @classmethod
    def edit_record(cls, token: str, record: dict, record_id: int) -> None:
        with DBConnectionHandler() as database:
            print("Editing record:", record, "with ID:", record_id)
            try:
                update_parts = ', '.join(
                    [f"{key} = :{key}" for key in record.keys()])
                
                print(update_parts)

                with database.get_engine().connect() as connection:
                    connection = connection.execution_options(
                        isolation_level="AUTOCOMMIT")

                    identificator_column = f'id_{token}'

                    sql = text("""UPDATE {token_str} SET {update_parts} WHERE {identificator_column} = :{identificator_column};""".format(
                        token_str=token, update_parts=update_parts, identificator_column=identificator_column))
                    
                    print(sql)

                    record[identificator_column] = record_id

                    connection.execute(sql, record)
            except Exception as exception:
                database.session.rollback()
                raise exception

    @classmethod
    def delete_record(cls, token: str, record_id: int) -> None:
        with DBConnectionHandler() as database:
            try:
                # Executar o SQL para inserir dados na tabela dinâmica
                with database.get_engine().connect() as connection:

                    connection = connection.execution_options(
                        isolation_level="AUTOCOMMIT")

                    identification_token = f"id_{token}"

                    sql = text("DELETE FROM {} WHERE {} = :record_id;".format(
                        token, identification_token))

                    connection.execute(sql, {'record_id': record_id})
            except Exception as exception:
                database.session.rollback()
                raise exception

    @classmethod
    def list_records(cls, token: str, filters: dict[str, Any] | None = None) -> List[dict]:
        with DBConnectionHandler() as db:
            try:
                with db.get_engine().connect() as conn:
                    conn = conn.execution_options(isolation_level="AUTOCOMMIT")

                    where_parts, params = [], {}
                    if filters:
                        for idx, (col, val) in enumerate(filters.items()):
                            key = f"p{idx}"

                            if val is None:                                 # IS NULL
                                where_parts.append(f"{col} IS NULL")

                            elif isinstance(val, (list, tuple)):           # IN (...)
                                placeholders = ", ".join(f":{key}_{i}" for i in range(len(val)))
                                where_parts.append(f"{col} IN ({placeholders})")
                                params.update({f"{key}_{i}": v for i, v in enumerate(val)})

                            else:                                          # =
                                where_parts.append(f"{col} = :{key}")
                                params[key] = val

                    where_sql = f" WHERE {' AND '.join(where_parts)}" if where_parts else ""
                    sql = text(f"SELECT * FROM {token}{where_sql};")

                    result = conn.execute(sql, params)
                    return [dict(row._mapping) for row in result]
            except Exception:
                db.session.rollback()
                raise

    @classmethod
    def list_specific_record(cls, token: str, record_id: int) -> List[dict]:
        with DBConnectionHandler() as database:
            try:
                with database.get_engine().connect() as connection:
                    connection = connection.execution_options(
                        isolation_level="AUTOCOMMIT")

                    id_column = f'id_{token}'
                    sql = text(
                        "SELECT * FROM {} WHERE {} = :record_id;".format(token, id_column))

                    response = connection.execute(
                        sql, {'record_id': record_id})

                    records = [dict(row._mapping) for row in response]

                    return records
            except Exception as exception:
                database.session.rollback()
                raise exception

    @classmethod
    def list_keys(cls, token: str) -> List[Tuple[str, str]]:

        with DBConnectionHandler() as database:
            try:
                engine = database.get_engine()
                inspector = inspect(engine)

                columns = inspector.get_columns(token.lower())

                # Retorna lista de tuplas: (nome_coluna, tipo_coluna)
                return [(col['name'], str(col['type'])) for col in columns]

            except Exception as exception:
                database.session.rollback()
                raise exception
