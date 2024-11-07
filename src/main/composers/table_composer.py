from src.infra.db.repositories.table_repository import TableRepository
from src.data.use_cases.table import TableList, TableRegister
from src.presentation.controllers.table_controller import TableListController, TableRegisterController


def table_list_composer():
    repository = TableRepository()
    use_case = TableList(repository)
    controller = TableListController(use_case)

    return controller.handle


def table_register_composer():
    repository = TableRepository()
    use_case = TableRegister(repository)
    controller = TableRegisterController(use_case)

    return controller.handle
