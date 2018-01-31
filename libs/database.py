from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr


class ExtendedBase:
    '''
    simplify sqlalchemy models declaration
    automaticaly generate tablename from class name,
    '''
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base(cls=ExtendedBase)
