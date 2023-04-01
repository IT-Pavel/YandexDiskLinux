import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Database():
    DATABASE_FILE = 'data.db3'
    DATABASE_CONNECTION_STRING = f'sqlite:///{DATABASE_FILE}'

    def __init__(self) -> None:
        Base = declarative_base()
        self.engine = db.create_engine(self.DATABASE_CONNECTION_STRING)
        self.__connection = self.engine
        self.__metadata = db.MetaData()


class FolderList(Base):
    __tablename__ = 'FolderList'

    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Path = db.Column(db.String, default='')
    Sync = db.Column(db.Boolean, default=True)
