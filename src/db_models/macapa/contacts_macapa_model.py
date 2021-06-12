from sqlalchemy import Column, Integer, String
from src.db_models.macapa import database
from sqlalchemy.types import DateTime
from datetime import datetime

class ContactsMacapa(database.Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    nome = Column(String(200), nullable=False)
    celular = Column(String(20), nullable=False)

    def __init__(self, nome: str, celular: str):
        self.nome = nome
        self.celular = celular
