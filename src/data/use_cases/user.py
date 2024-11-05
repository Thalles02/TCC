# pylint: disable=broad-exception-raised
from typing import Dict, List
from src.domain.use_cases.user import UserFinder as UserFinderInterface
from src.domain.use_cases.user import UserRegister as UserRegisterInterface
from src.data.interfaces.users_repository import UsersRepositoryInterface
from src.domain.models.user import Users
from src.errors.types import HttpNotFoundError, HttpBadRequestError


class UserFinder(UserFinderInterface):
    def __init__(self, users_repository: UsersRepositoryInterface) -> None:
        self.__users_repository = users_repository

    def find(self, first_name: str) -> Dict:
        self.__validate_name(first_name)
        users = self.__search_user(first_name)
        response = self.__format_response(users)
        return response

    @classmethod
    def __validate_name(cls, first_name: str) -> None:
        if not first_name.isalpha():
            raise HttpBadRequestError('Nome invalido para a busca')

        if len(first_name) > 18:
            raise HttpBadRequestError('Nome muito grande para busca')

    def __search_user(self, first_name: str) -> List[Users]:
        users = self.__users_repository.select_user(first_name)
        if users == []:
            raise HttpNotFoundError('Usuario nao encontrado')
        return users

    @classmethod
    def __format_response(cls, users: List[Users]) -> Dict:
        attributes = []
        for user in users:
            attributes.append(
                {"first_name": user.first_name, "email_address": user.email_address}
            )

        response = {
            "type": "Users",
            "count": len(users),
            "attributes": attributes
        }

        return response


class UserRegister(UserRegisterInterface):
    def __init__(self, user_repository: UsersRepositoryInterface) -> None:
        self.__user_repository = user_repository

    def register(self, first_name: str, last_name: str, email_address: str) -> Dict:
        self.__validate_name(first_name)
        self.__validate_name(last_name)

        self.__registry_user_informations(first_name, last_name, email_address)
        response = self.__format_response(first_name, last_name, email_address)
        return response

    @classmethod
    def __validate_name(cls, first_name: str) -> None:
        if not first_name.isalpha():
            raise HttpBadRequestError('Nome invalido para o cadastro')

        if len(first_name) > 18:
            raise HttpBadRequestError('Nome muito grande para o cadastro')

    def __registry_user_informations(self, first_name: str, last_name: str, email_address: str) -> None:
        self.__user_repository.insert_user(
            first_name, last_name, email_address)

    @classmethod
    def __format_response(cls, first_name: str, last_name: str, email_address: str) -> Dict:
        response = {
            "type": "Users",
            "count": 1,
            "attributes": {
                "first_name": first_name,
                "last_name": last_name,
                "email_address": email_address
            }
        }
        return response
