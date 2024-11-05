from src.infra.db.tests.users_repository import UsersRepositorySpy
from .user_register import UserRegister


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
