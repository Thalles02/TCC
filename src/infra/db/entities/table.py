from sqlalchemy import Column, String
from src.infra.db.settings.base import Base


class Table(Base):
    __tablename__ = "flowtable"

    token = Column(String, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"Users [token={self.token}, table_name={self.name}]"
