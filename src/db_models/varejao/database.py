from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from src.config import CONNECTION_STRING_POSTGRES, CONNECTION_STRING_POSTGRES_DEV, PRODUCTION


class DatabaseVarejao:
    def __init__(self):
        self.engine = create_engine(CONNECTION_STRING_POSTGRES if PRODUCTION else CONNECTION_STRING_POSTGRES_DEV)
        self.db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))
        self.base = declarative_base()
        self.base.query = self.db_session.query_property()

    def init_db(self):
        self.Base.metadata.create_all(bind=self.engine)

database_varejao = DatabaseVarejao()

