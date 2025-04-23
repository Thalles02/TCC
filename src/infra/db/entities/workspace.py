from sqlalchemy import Column, String, Integer
from src.infra.db.settings.base import Base


class Workspace(Base):
    __tablename__ = "workspace"

    id_workspace = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"Workspace [id_workspace={self.id_workspace}, workspace_name={self.name}]"
