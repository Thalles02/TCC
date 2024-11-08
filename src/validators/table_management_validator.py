from cerberus import Validator
from src.errors.types import HttpUnprocessableEntityError


def table_management_token_validator(request: any):

    body_validator = Validator({
        "token": {"type": "string", "required": True, "empty": False},
    })
    response = body_validator.validate(request.json)

    if response is False:
        raise HttpUnprocessableEntityError(body_validator.errors)


def table_management_add_column_validator(request: any):

    body_validator = Validator({
        "token": {"type": "string", "required": True, "empty": False},
        "column_definition": {
            "type": "dict",
            "required": True,
            "empty": False,
            "schema": {
                "column_name": {"type": "string", "required": True, "empty": False},
                "column_type": {"type": "string", "required": True, "empty": False, "allowed": ["INTEGER", "VARCHAR(255)", "VARCHAR(1000)", "VARCHAR(3000)", "BOOLEAN", "DATE", "TIMESTAMP", "DECIMAL"]}
            }
        },
    })
    response = body_validator.validate(request.json)

    if response is False:
        raise HttpUnprocessableEntityError(body_validator.errors)


def table_management_insert_record_validator(request: any):

    body_validator = Validator({
        "token": {"type": "string", "required": True, "empty": False},
        "data": {
            "type": "dict",
            "required": True,
            "empty": False
        },
    })
    response = body_validator.validate(request.json)

    if response is False:
        raise HttpUnprocessableEntityError(body_validator.errors)


def table_management_edit_record_validator(request: any):

    body_validator = Validator({
        "token": {"type": "string", "required": True, "empty": False},
        "data": {
            "type": "dict",
            "required": True,
            "empty": False
        },
        "record_id": {"type": "integer", "required": True, "empty": False},
    })
    response = body_validator.validate(request.json)

    if response is False:
        raise HttpUnprocessableEntityError(body_validator.errors)


def table_management_token_and_id_record_validator(request: any):

    body_validator = Validator({
        "token": {"type": "string", "required": True, "empty": False},
        "record_id": {"type": "integer", "required": True, "empty": False},
    })
    response = body_validator.validate(request.json)

    if response is False:
        raise HttpUnprocessableEntityError(body_validator.errors)
