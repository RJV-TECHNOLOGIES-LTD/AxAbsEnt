from sqlalchemy import Column, Integer, String, Text, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Dimension(Base):
    __tablename__ = 'dimensions'

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    formulation = Column(Text)
    metadata = Column(JSON)
    parent_1 = Column(String)
    parent_2 = Column(String)
