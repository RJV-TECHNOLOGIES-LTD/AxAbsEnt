from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Dimension

def get_engine(db_url='sqlite:///axabsent_registry.db'):
    return create_engine(db_url)

def init_db(engine):
    Base.metadata.create_all(engine)

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
