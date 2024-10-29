from .user_repository import UsersRepository


def test_insert_user():

    mocked_first_name = 'first'
    mocked_last_name = 'last'
    mocked_email_address = 'test@test'
    users_repository = UsersRepository()
    users_repository.insert_user(
        mocked_first_name, mocked_last_name, mocked_email_address)
