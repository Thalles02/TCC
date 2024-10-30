from typing import List
from src.domain.models.user import Users


class UsersRepositorySpy:

    def __init__(self) -> None:
        self.insert_user_attributes = {}
        self.select_user_attributes = {}

    def insert_user(self, first_name: str, last_name: str, email_address: str) -> None:
        self.insert_user_attributes["first_name"] = first_name
        self.insert_user_attributes["last_name"] = last_name
        self.insert_user_attributes["email_address"] = email_address

    def select_user(self, first_name: str) -> List[Users]:
        self.select_user_attributes["first_name"] = first_name
        return [
            Users(23, first_name, 'last', 'teste1@gmail.com'),
            Users(23, first_name, 'last_2', 'teste2@gmail.com')
        ]
