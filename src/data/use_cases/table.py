# pylint: disable=broad-exception-raised
from typing import Dict, List
from src.domain.use_cases.table import TableRegister as TableRegisterInterface
from src.domain.use_cases.table import TableList as TableListInterface
from src.data.interfaces.table_repository import TableRepositoryInterface
from src.domain.models.table import Table
from src.errors.types import HttpNotFoundError, HttpBadRequestError


class TableRegister(TableRegisterInterface):
    def __init__(self, table_repository: TableRepositoryInterface) -> None:
        self.__table_repository = table_repository

    def register(self, token: str, name: str) -> Dict:
        self.__validade_token(token)

        self.__registry_table_informations(token, name)
        response = self.__format_response(token, name)
        return response

    @classmethod
    def __validade_token(cls, token: str) -> None:
        if len(token) != 20:
            raise HttpBadRequestError(
                'Quantidade de caracteres inválidas para o token')

    def __registry_table_informations(self, token: str, name: str) -> None:
        self.__table_repository.insert_table(token, name)

    @classmethod
    def __format_response(cls, token: str, name: str) -> Dict:
        response = {
            "type": "Table",
            "count": 1,
            "attributes": {
                "token": token,
                "name": name
            }
        }
        return response


class TableList(TableListInterface):
    def __init__(self, table_repository: TableListInterface) -> None:
        self.__table_repository = table_repository

    def list_tables(self) -> Dict:
        tables = self.__search_table()
        response = self.__format_response(tables)
        return response

    def __search_table(self) -> List[Table]:
        tables = self.__table_repository.list_tables()
        if tables == []:
            raise HttpNotFoundError('Nenhuma Tabela encontrada')
        return tables

    @classmethod
    def __format_response(cls, table: List[Table]) -> Dict:
        attributes = []
        for item in table:
            attributes.append(
                {"token": item.token, "name": item.name}
            )

        response = {
            "type": "Tables",
            "count": len(table),
            "attributes": attributes
        }

        return response
