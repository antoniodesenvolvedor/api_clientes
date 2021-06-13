from sqlalchemy import Column, Integer, String, Text
from src.db_models.macapa.database import database_macapa
from sqlalchemy.types import DateTime
from datetime import datetime

class ContactsMacapa(database_macapa.Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    nome = Column(String(200), nullable=False)
    celular = Column(String(20), nullable=False)

    def __init__(self, nome: str, celular: str):
        self.nome = nome
        self.celular = celular


class UserMacapa(database_macapa.Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    public_id = Column(String(50), unique = True)
    name = Column(String(100))
    email = Column(String(70), unique = True)
    password = Column(Text())
