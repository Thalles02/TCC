# pylint: disable=broad-exception-raised
from typing import Dict, List
from src.domain.use_cases.table_management import TableManagementAddColumn as TableManagementAddColumnInterface
from src.domain.use_cases.table_management import TableManagementInsertRecord as TableManagementInsertRecordInterface
from src.domain.use_cases.table_management import TableManagementEditRecord as TableManagementEditRecordInterface
from src.domain.use_cases.table_management import TableManagementDeleteRecord as TableManagementDeleteRecordInterface
from src.domain.use_cases.table_management import TableManagementListKeys as TableManagementListKeysInterface
from src.domain.use_cases.table_management import TableManagementListRecords as TableManagementListRecordsInterface
from src.domain.use_cases.table_management import TableManagementListSpecificRecord as TableManagementListSpecificRecordInterface
from src.data.interfaces.table_management_repository import TableManagementRepositoryInterface
from src.errors.types import HttpBadRequestError, HttpNotFoundError


class TableListKeys(TableManagementListKeysInterface):
    def __init__(self, table_repository: TableManagementRepositoryInterface) -> None:
        self.__table_repository = table_repository

    def list_keys(self, token: str) -> List[str]:
        self.__validade_token(token)

        list_response = self.__list_keys(token)
        response = self.__format_response(list_response)
        return response

    @classmethod
    def __validade_token(cls, token: str) -> None:
        if len(token) != 20 and token != 'workspacetables':
            raise HttpBadRequestError(
                'Quantidade de caracteres inválidas para o token')

    def __list_keys(self, token: str) -> List[str]:
        response = self.__table_repository.list_keys(token)

        return response

    @classmethod
    def __format_response(cls, keys: List[str]) -> Dict:
        response = {
            "type": "Table Keys",
            "count": len(keys),
            "attributes": keys
        }

        return response


class TableAddColumn(TableManagementAddColumnInterface):
    def __init__(self, table_repository: TableManagementRepositoryInterface) -> None:
        self.__table_repository = table_repository

    def add_column(self, token: str, column_definition: dict) -> Dict:
        self.__validade_token(token)
        self.__validate_column(token, column_definition)

        self.__registry_column(token, column_definition)
        response = self.__format_response(token, column_definition)
        return response

    @classmethod
    def __validade_token(cls, token: str) -> None:
        if len(token) != 20 and token != 'workspacetables':
            raise HttpBadRequestError(
                'Quantidade de caracteres inválidas para o token')

    def __validate_column(self, token: str, column_definition: dict) -> None:
        keys = self.__table_repository.list_keys(token)
        if column_definition['column_name'] in keys:
            raise HttpBadRequestError(
                'Essa coluna já existe nesta tabela')

    def __registry_column(self, token: str, column_definition: dict) -> None:
        self.__table_repository.add_column(token, column_definition)

    @classmethod
    def __format_response(cls, token: str, column_definition: dict) -> Dict:
        response = {
            "type": "Table",
            "count": 1,
            "attributes": {
                "token": token,
                "column_name": column_definition['column_name'],
                "column_type": column_definition['column_type']
            }
        }
        return response


class TableInsertRecord(TableManagementInsertRecordInterface):
    def __init__(self, table_repository: TableManagementRepositoryInterface) -> None:
        self.__table_repository = table_repository

    def insert_record(self, token: str, record: dict) -> Dict:
        self.__validade_token(token)
        self.__validate_columns(token, record)

        self.__registry_record(token, record)
        response = self.__format_response(token, record)
        return response

    @classmethod
    def __validade_token(cls, token: str) -> None:
        if len(token) != 20 and token != 'workspacetables':
            raise HttpBadRequestError(
                'Quantidade de caracteres inválidas para o token')

    def __validate_columns(self, token: str, record: dict) -> None:
        keys = self.__table_repository.list_keys(token)
        for i in record.keys():
            if i not in keys:
                raise HttpBadRequestError(
                    f"Não existe a coluna {i} nesta tabela")

    def __registry_record(self, token: str, record: dict) -> None:
        self.__table_repository.insert_record(token, record)

    @classmethod
    def __format_response(cls, token: str, record: dict) -> Dict:
        response = {
            "type": "Record",
            "count": 1,
            "attributes": {
                "token": token,
                "data": record
            }
        }
        return response


class TableEditRecord(TableManagementEditRecordInterface):
    def __init__(self, table_repository: TableManagementRepositoryInterface) -> None:
        self.__table_repository = table_repository

    def edit_record(self, token: str, record: dict, record_id: int) -> Dict:
        self.__validade_token(token)
        self.__validate_columns(token, record)

        self.__edit_record(token, record, record_id)
        response = self.__format_response(token, record)
        return response

    @classmethod
    def __validade_token(cls, token: str) -> None:
        if len(token) != 20 and token != 'workspacetables':
            raise HttpBadRequestError(
                'Quantidade de caracteres inválidas para o token')

    def __validate_columns(self, token: str, record: dict) -> None:
        keys = self.__table_repository.list_keys(token)
        for i in record.keys():
            if i not in keys:
                raise HttpBadRequestError(
                    f"Não existe a coluna {i} nesta tabela")

    def __edit_record(self, token: str, record: dict, record_id: int) -> None:
        self.__table_repository.edit_record(token, record, record_id)

    @classmethod
    def __format_response(cls, token: str, record: dict) -> Dict:
        response = {
            "type": "Record",
            "count": 1,
            "attributes": {
                "token": token,
                "data": record
            }
        }
        return response


class TableDeleteRecord(TableManagementDeleteRecordInterface):
    def __init__(self, table_repository: TableManagementRepositoryInterface) -> None:
        self.__table_repository = table_repository

    def delete_record(self, token: str, record_id: int) -> None:
        self.__validade_token(token)

        self.__delete_record(token, record_id)
        response = self.__format_response(token, record_id)
        return response

    @classmethod
    def __validade_token(cls, token: str) -> None:
        if len(token) != 20 and token != 'workspacetables':
            raise HttpBadRequestError(
                'Quantidade de caracteres inválidas para o token')

    def __delete_record(self, token: str, record_id: int) -> None:
        self.__table_repository.delete_record(token, record_id)

    @classmethod
    def __format_response(cls, token: str, record_id: int) -> Dict:
        response = {
            "type": "Delete Record",
            "count": 1,
            "attributes": {
                "token": token,
                "record_id": record_id
            }
        }
        return response


class TableListRecords(TableManagementListRecordsInterface):
    def __init__(self, table_repository: TableManagementRepositoryInterface) -> None:
        self.__table_repository = table_repository

    def list_records(self, token: str, filter: dict) -> List[dict]:
        records = self.__search_records(token, filter)
        response = self.__format_response(records)
        return response

    def __search_records(self, token: str, filter: dict) -> List[dict]:
        records = self.__table_repository.list_records(token, filter)
        if len(records) == 0:
            raise HttpNotFoundError('Nenhum registro encontrado')
        return records

    @classmethod
    def __format_response(cls, records: List[dict]) -> Dict:

        response = {
            "type": "List Records",
            "records": records
        }

        return response


class TableListSpecificRecord(TableManagementListSpecificRecordInterface):
    def __init__(self, table_repository: TableManagementRepositoryInterface) -> None:
        self.__table_repository = table_repository

    def list_specific_record(self, token: str, record_id: int) -> List[dict]:
        records = self.__search_records(token, record_id)
        response = self.__format_response(records)
        return response

    def __search_records(self, token: str, record_id: int) -> List[dict]:
        records = self.__table_repository.list_specific_record(
            token, record_id)
        if len(records) == 0:
            raise HttpNotFoundError('Nenhum registro encontrado')
        return records

    @classmethod
    def __format_response(cls, records: List[dict]) -> Dict:

        response = {
            "type": "List Records",
            "records": records
        }

        return response
