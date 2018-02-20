from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

from . import settings


engine = create_engine(settings.DATABASE)
Session = sessionmaker(bind=engine)


class ExtendedBase:
    '''
    simplify sqlalchemy models declaration
    automaticaly generate tablename from class name,
    '''
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(cls=ExtendedBase)


def initDB():
    Base.metadata.create_all(engine)
