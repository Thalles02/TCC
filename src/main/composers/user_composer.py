from src.infra.db.repositories.users_repository import UsersRepository
from src.data.use_cases.user import UserFinder, UserRegister
from src.presentation.controllers.user_controller import UserFinderController, UserRegisterController


def user_finder_composer():
    repository = UsersRepository()
    use_case = UserFinder(repository)
    controller = UserFinderController(use_case)

    return controller.handle


def user_register_composer():
    repository = UsersRepository()
    use_case = UserRegister(repository)
    controller = UserRegisterController(use_case)

    return controller.handle
