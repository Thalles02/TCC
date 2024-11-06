from src.infra.db.tests.users_repository import UsersRepositorySpy
from ..user import UserFinder, UserRegister


# Testes para o caso de uso UseFinder
def test_find():
    first_name = 'meuNome'

    repo = UsersRepositorySpy()
    user_finder = UserFinder(repo)

    response = user_finder.find(first_name)

    assert repo.select_user_attributes["first_name"] == first_name

    assert response["type"] == "Users"
    assert response["count"] == len(response["attributes"])
    assert response["attributes"]


def test_find_error_in_valid_name():
    first_name = 'meuNome123'

    repo = UsersRepositorySpy()
    user_finder = UserFinder(repo)

    try:
        user_finder.find(first_name)
        assert False
    except Exception as expection:
        assert str(expection) == "Nome invalido para a busca"


def test_find_error_in_long_name():
    first_name = 'meuNomeahlfksjhfsjkalhkfjhsalfkshfkljshalkjsh'

    repo = UsersRepositorySpy()
    user_finder = UserFinder(repo)

    try:
        user_finder.find(first_name)
        assert False
    except Exception as expection:
        assert str(expection) == "Nome muito grande para busca"


def test_find_error_user_not_found():
    class UsersRepositoryError(UsersRepositorySpy):
        def select_user(self, first_name: str):
            return []

    first_name = 'meuNome'

    repo = UsersRepositoryError()
    user_finder = UserFinder(repo)

    try:
        user_finder.find(first_name)
        assert False
    except Exception as expection:
        assert str(expection) == "Usuario nao encontrado"


# Testes para o caso de uso UserRegister
def test_register():
    first_name = "ola"
    last_name = "aqui"
    email_address = "teste@teste"

    repo = UsersRepositorySpy()
    user_register = UserRegister(repo)

    response = user_register.register(first_name, last_name, email_address)

    assert repo.insert_user_attributes["first_name"] == first_name
    assert repo.insert_user_attributes["last_name"] == last_name
    assert repo.insert_user_attributes["email_address"] == email_address

    assert response["type"] == "Users"
    assert response["count"] == 1
    assert response["attributes"]


def test_register_first_name_error():
    first_name = "ola3131313"
    last_name = "aqui"
    email_address = "teste@teste"

    repo = UsersRepositorySpy()
    user_register = UserRegister(repo)

    try:
        user_register.register(first_name, last_name, email_address)
        assert False
    except Exception as exception:
        assert str(exception) == "Nome invalido para o cadastro"
