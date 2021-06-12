from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.server.config import CONNECTION_STRING_MYSQL, CONNECTION_STRING_MYSQL_DEV, PRODUCTION


class DatabaseMacapa:
    def __init__(self):
        self.engine = create_engine(CONNECTION_STRING_MYSQL if PRODUCTION else CONNECTION_STRING_MYSQL_DEV)
        self.db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))
        self.Base = declarative_base()
        self.Base.query = self.db_session.query_property()

    def init_db(self):
        self.Base.metadata.create_all(bind=self.engine)

database_macapa = DatabaseMacapa()

