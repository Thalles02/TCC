from cerberus import Validator
from src.errors.types import HttpUnprocessableEntityError


def user_finder_validator(request: any):

    query_validator = Validator({
        "first_name": {"type": "string", "required": True, "empty": False}
    })
    response = query_validator.validate(request.args)

    if response is False:
        raise HttpUnprocessableEntityError(query_validator.errors)


def user_register_validator(request: any):

    body_validator = Validator({
        "first_name": {"type": "string", "required": True, "empty": False},
        "last_name": {"type": "string", "required": True, "empty": False},
        "email_address": {"type": "string", "required": True, "empty": False}
    })
    response = body_validator.validate(request.json)

    if response is False:
        raise HttpUnprocessableEntityError(body_validator.errors)
