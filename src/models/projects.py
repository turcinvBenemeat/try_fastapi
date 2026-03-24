from sqlalchemy import Boolean, Column, Integer, String

from src.database import Base

# TODO: Change structure

class Project(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean, default=False)