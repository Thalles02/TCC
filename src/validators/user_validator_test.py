from .user_validator import user_register_validator


class MockRequest:
    def __init__(self) -> None:
        self.json = None


def test_user_register_validator():
    print()
    request = MockRequest()
    request.json = {
        "first_name": "meuNome",
        "last_name": "algumaCoisa",
        "email_address": "thalles.martins75@gmail.com"
    }

    user_register_validator(request)
