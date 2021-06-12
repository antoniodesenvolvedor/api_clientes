from sqlalchemy import Column, Integer, String, Text
from src.db_models.varejao.database import database_varejao
from sqlalchemy.types import DateTime
from datetime import datetime

class ContactsVarejao(database_varejao.Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    celular = Column(String(13), nullable=False)

    def __init__(self, nome: str, celular: str):
        self.nome = nome
        self.celular = celular



class UserVarejao(database_varejao.Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    public_id = Column(String(50), unique = True)
    name = Column(String(100))
    email = Column(String(70), unique = True)
    password = Column(Text())

