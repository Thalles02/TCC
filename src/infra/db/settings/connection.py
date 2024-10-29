from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBConnectionHandler:

    def __init__(self) -> None:
        self.__connection_string = "{}://{}:{}@{}:{}/{}".format(
            'postgresql+psycopg2',  # Driver para PostgreSQL
            'postgres',                 # Usuário do banco de dados
            'postgres',           # Senha do banco de dados
            'localhost',            # Host do banco de dados
            '5432',                 # Porta padrão para PostgreSQL
            'flow_database'        # Nome do banco de dados
        )
        self.__engine = self.__create_database_engine()
        self.session = None

    def __create_database_engine(self):
        engine = create_engine(self.__connection_string)
        return engine

    def get_engine(self):
        return self.__engine

    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        self.session = session_make()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
