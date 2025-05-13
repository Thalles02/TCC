from src.presentation.interfaces.controller_interface import ControllerInterface
from src.domain.use_cases.table_management import TableManagementListKeys as TableManagementListKeysInterface
from src.domain.use_cases.table_management import TableManagementAddColumn as TableManagementAddColumnInterface
from src.domain.use_cases.table_management import TableManagementInsertRecord as TableManagementInsertRecordInterface
from src.domain.use_cases.table_management import TableManagementEditRecord as TableManagementEditRecordInterface
from src.domain.use_cases.table_management import TableManagementDeleteRecord as TableManagementDeleteRecordInterface
from src.domain.use_cases.table_management import TableManagementListRecords as TableManagementListRecordsInterface
from src.domain.use_cases.table_management import TableManagementListSpecificRecord as TableManagementListSpecificRecordInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class TableListKeysController(ControllerInterface):
    def __init__(self, use_case: TableManagementListKeysInterface) -> None:
        self.__use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:

        token = http_request.body["token"]

        response = self.__use_case.list_keys(token)

        return HttpResponse(
            status_code=200,
            body={"data": response}
        )


class TableAddColumnController(ControllerInterface):
    def __init__(self, use_case: TableManagementAddColumnInterface) -> None:
        self.__use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:

        token = http_request.body["token"]
        column_definition = http_request.body["column_definition"]

        response = self.__use_case.add_column(token, column_definition)

        return HttpResponse(
            status_code=200,
            body={"data": response}
        )


class TableInserRecordController(ControllerInterface):
    def __init__(self, use_case: TableManagementInsertRecordInterface) -> None:
        self.__use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:

        token = http_request.body["token"]
        record = http_request.body["data"]

        response = self.__use_case.insert_record(token, record)

        return HttpResponse(
            status_code=200,
            body={"data": response}
        )


class TableEditRecordController(ControllerInterface):
    def __init__(self, use_case: TableManagementEditRecordInterface) -> None:
        self.__use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:

        token = http_request.body["token"]
        record = http_request.body["data"]
        record_id = http_request.body["record_id"]

        response = self.__use_case.edit_record(token, record, record_id)

        return HttpResponse(
            status_code=200,
            body={"data": response}
        )


class TableDeleteRecordController(ControllerInterface):
    def __init__(self, use_case: TableManagementDeleteRecordInterface) -> None:
        self.__use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:

        token = http_request.body["token"]
        record_id = http_request.body["record_id"]

        response = self.__use_case.delete_record(token, record_id)

        return HttpResponse(
            status_code=200,
            body={"data": response}
        )


class TableListRecordsController(ControllerInterface):
    def __init__(self, use_case: TableManagementListRecordsInterface) -> None:
        self.__use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:

        token = http_request.body["token"]

        filter = http_request.body["filter"]

        print(filter)

        response = self.__use_case.list_records(token, filter)

        return HttpResponse(
            status_code=200,
            body={"data": response}
        )


class TableListSpecificRecordController(ControllerInterface):
    def __init__(self, use_case: TableManagementListSpecificRecordInterface) -> None:
        self.__use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:

        token = http_request.body["token"]
        record_id = http_request.body["record_id"]

        response = self.__use_case.list_specific_record(token, record_id)

        return HttpResponse(
            status_code=200,
            body={"data": response}
        )
