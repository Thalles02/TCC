from src.infra.db.repositories.workspace_repository import WorkspaceRepository
from src.data.use_cases.workspace import WorkspaceList, WorkspaceRegister
from src.presentation.controllers.workspace_controller import WorkspaceListController, WorkspaceRegisterController


def workspace_list_composer():
    repository = WorkspaceRepository()
    use_case = WorkspaceList(repository)
    controller = WorkspaceListController(use_case)

    return controller.handle


def workspace_register_composer():
    repository = WorkspaceRepository()
    use_case = WorkspaceRegister(repository)
    controller = WorkspaceRegisterController(use_case)

    return controller.handle
