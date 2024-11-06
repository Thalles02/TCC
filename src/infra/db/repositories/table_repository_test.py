# import pytest
from sqlalchemy import text
from src.infra.db.settings.connection import DBConnectionHandler
from .table_repository import TableRepository
from src.helpers.helpers import generate_token
import pytest

db_connection_handler = DBConnectionHandler()
connection = db_connection_handler.get_engine().connect()


@pytest.mark.skip(reason="Sensive test")
def test_insert_table():
    mocked_token = generate_token()
    mocked_name = 'Tabela de Tarefas'

    table_repository = TableRepository()
    table_repository.insert_table(
        mocked_token, mocked_name)

    sql = '''
        SELECT * FROM flowtable
        WHERE token = '{}'
        AND name = '{}'
    '''.format(mocked_token, mocked_name)
    response = connection.execute(text(sql))
    registry = response.fetchall()[0]

    assert registry.token == mocked_token
    assert registry.name == mocked_name

    connection.execute(text(f'''
        DELETE FROM flowtable WHERE token = '{registry.token}'
    '''))
    connection.commit()


@pytest.mark.skip(reason="Sensive test")
def test_list_tables():
    mocked_token = generate_token()
    mocked_name = 'last_2'

    sql = '''
        INSERT INTO flowtable (token, name) VALUES ('{}', '{}')
    '''.format(mocked_token, mocked_name)
    connection.execute(text(sql))
    connection.commit()

    table_repository = TableRepository()
    response = table_repository.list_tables()

    assert response[0].token == mocked_token
    assert response[0].name == mocked_name

    connection.execute(text(f'''
        DELETE FROM flowtable WHERE token = '{response[0].token}'
    '''))
    connection.commit()
