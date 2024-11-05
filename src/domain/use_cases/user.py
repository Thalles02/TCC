from abc import ABC, abstractmethod
from typing import Dict


class UserFinder(ABC):
    @abstractmethod
    def find(self, first_name: str) -> Dict: pass


class UserRegister(ABC):
    @abstractmethod
    def register(self, first_name: str, last_name: str,
                 email_address: str) -> Dict: pass
