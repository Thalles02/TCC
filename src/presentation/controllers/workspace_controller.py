from src.presentation.interfaces.controller_interface import ControllerInterface
from src.domain.use_cases.workspace import WorkspaceList as WorkspaceListInterface
from src.domain.use_cases.workspace import WorkspaceRegister as WorkspaceRegisterInterface
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse


class WorkspaceRegisterController(ControllerInterface):
    def __init__(self, use_case: WorkspaceRegisterInterface) -> None:
        self.__use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        name = http_request.body["name"]

        response = self.__use_case.register(name)

        return HttpResponse(
            status_code=200,
            body={"data": response}
        )

class WorkspaceListController(ControllerInterface):
    def __init__(self, use_case: WorkspaceListInterface) -> None:
        self.__use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:

        response = self.__use_case.list_workspaces()

        return HttpResponse(
            status_code=200,
            body={"data": response}
        )