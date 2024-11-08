from flask import Blueprint, request, jsonify

# Import adapters
from src.main.adapters.request_adapter import request_adapter

# Import composers
from src.main.composers.user_composer import user_finder_composer, user_register_composer
from src.main.composers.table_composer import table_list_composer, table_register_composer
from src.main.composers.table_management_composer import table_add_column_composer, table_insert_record_composer, table_edit_record_composer, table_delete_record_composer, table_list_keys_composer, table_list_records_composer, table_list_specific_record_composer

# Import Validators
from src.validators.user_validator import user_register_validator, user_finder_validator
from src.validators.table_validator import table_register_validator
from src.validators.table_management_validator import table_management_add_column_validator, table_management_insert_record_validator, table_management_edit_record_validator, table_management_token_and_id_record_validator, table_management_token_validator

# Import error handler
from src.errors.error_handler import handle_errors


api_route_bp = Blueprint("api_routes", __name__)


@api_route_bp.route("/user/find", methods=["GET"])
def find_user():
    http_response = None

    try:
        user_finder_validator(request)
        http_response = request_adapter(request, user_finder_composer())
    except Exception as exception:
        http_response = handle_errors(exception)

    return jsonify(http_response.body), http_response.status_code


@api_route_bp.route("/user", methods=["POST"])
def register_user():
    http_response = None

    try:
        user_register_validator(request)
        http_response = request_adapter(request, user_register_composer())
    except Exception as exception:
        http_response = handle_errors(exception)

    return jsonify(http_response.body), http_response.status_code


@api_route_bp.route("/table/list", methods=["GET"])
def list_table():
    http_response = None

    try:
        http_response = request_adapter(request, table_list_composer())
    except Exception as exception:
        http_response = handle_errors(exception)

    return jsonify(http_response.body), http_response.status_code


@api_route_bp.route("/table/register", methods=["POST"])
def register_table():
    http_response = None

    try:
        table_register_validator(request)
        http_response = request_adapter(request, table_register_composer())
    except Exception as exception:
        http_response = handle_errors(exception)

    return jsonify(http_response.body), http_response.status_code


@api_route_bp.route("/table/list-keys", methods=["POST"])
def list_keys_table_management():
    http_response = None

    try:
        table_management_token_validator(request)
        http_response = request_adapter(request, table_list_keys_composer())
    except Exception as exception:
        http_response = handle_errors(exception)

    return jsonify(http_response.body), http_response.status_code


@api_route_bp.route("/table/add-column", methods=["POST"])
def add_column_table_management():
    http_response = None

    try:
        table_management_add_column_validator(request)
        http_response = request_adapter(request, table_add_column_composer())
    except Exception as exception:
        http_response = handle_errors(exception)

    return jsonify(http_response.body), http_response.status_code


@api_route_bp.route("/table/insert-record", methods=["POST"])
def insert_record_table_management():
    http_response = None

    try:
        table_management_insert_record_validator(request)
        http_response = request_adapter(
            request, table_insert_record_composer())
    except Exception as exception:
        http_response = handle_errors(exception)

    return jsonify(http_response.body), http_response.status_code


@api_route_bp.route("/table/edit-record", methods=["POST"])
def edit_record_table_management():
    http_response = None

    try:
        table_management_edit_record_validator(request)
        http_response = request_adapter(
            request, table_edit_record_composer())
    except Exception as exception:
        http_response = handle_errors(exception)

    return jsonify(http_response.body), http_response.status_code


@api_route_bp.route("/table/delete-record", methods=["POST"])
def delete_record_table_management():
    http_response = None

    try:
        table_management_token_and_id_record_validator(request)
        http_response = request_adapter(
            request, table_delete_record_composer())
    except Exception as exception:
        http_response = handle_errors(exception)

    return jsonify(http_response.body), http_response.status_code


@api_route_bp.route("/table/list-records", methods=["POST"])
def list_records_table_management():
    http_response = None

    try:
        table_management_token_validator(request)
        http_response = request_adapter(
            request, table_list_records_composer())
    except Exception as exception:
        http_response = handle_errors(exception)

    return jsonify(http_response.body), http_response.status_code


@api_route_bp.route("/table/list-specific-record", methods=["POST"])
def list_specific_record_table_management():
    http_response = None

    try:
        table_management_token_and_id_record_validator(request)
        http_response = request_adapter(
            request, table_list_specific_record_composer())
    except Exception as exception:
        http_response = handle_errors(exception)

    return jsonify(http_response.body), http_response.status_code
