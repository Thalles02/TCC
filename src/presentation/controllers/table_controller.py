from src.presentation.interfaces.controller_interface import ControllerInterface
from src.domain.use_cases.table import TableList as TableListInterface
from src.domain.use_cases.table import TableRegister as TableRegisterInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.helpers.helpers import generate_token


class TableListController(ControllerInterface):
    def __init__(self, use_case: TableListInterface) -> None:
        self.__use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:

        response = self.__use_case.list_tables()

        return HttpResponse(
            status_code=200,
            body={"data": response}
        )


class TableRegisterController(ControllerInterface):
    def __init__(self, use_case: TableRegisterInterface) -> None:
        self.__use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        token = generate_token()
        name = http_request.body["name"]

        response = self.__use_case.register(token, name)

        return HttpResponse(
            status_code=200,
            body={"data": response}
        )
