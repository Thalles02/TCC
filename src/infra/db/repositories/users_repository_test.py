import pytest
from sqlalchemy import text
from src.infra.db.settings.connection import DBConnectionHandler
from .users_repository import UsersRepository

db_connection_handler = DBConnectionHandler()
connection = db_connection_handler.get_engine().connect()


@pytest.mark.skip(reason="Sensive test")
def test_insert_user():
    mocked_first_name = 'first'
    mocked_last_name = 'last'
    mocked_email_address = 'teste@teste'

    users_repository = UsersRepository()
    users_repository.insert_user(
        mocked_first_name, mocked_last_name, mocked_email_address)

    sql = '''
        SELECT * FROM users
        WHERE first_name = '{}'
        AND last_name = '{}'
        AND email_address = '{}'
    '''.format(mocked_first_name, mocked_last_name, mocked_email_address)
    response = connection.execute(text(sql))
    registry = response.fetchall()[0]

    assert registry.first_name == mocked_first_name
    assert registry.last_name == mocked_last_name
    assert registry.email_address == mocked_email_address

    connection.execute(text(f'''
        DELETE FROM users WHERE id = {registry.id}
    '''))
    connection.commit()


@pytest.mark.skip(reason="Sensive test")
def test_select_user():
    mocked_first_name = 'first_2'
    mocked_last_name = 'last_2'
    mocked_email_address = 'teste@teste'

    sql = '''
        INSERT INTO users (first_name, last_name, email_address) VALUES ('{}', '{}', '{}')
    '''.format(mocked_first_name, mocked_last_name, mocked_email_address)
    connection.execute(text(sql))
    connection.commit()

    users_repository = UsersRepository()
    response = users_repository.select_user(mocked_first_name)

    assert response[0].first_name == mocked_first_name
    assert response[0].last_name == mocked_last_name
    assert response[0].email_address == mocked_email_address

    connection.execute(text(f'''
        DELETE FROM users WHERE id = {response[0].id}
    '''))
    connection.commit()
