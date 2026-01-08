from sqlalchemy import Column, Integer, String, Boolean, Float
from .database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(Integer)
    correntista = Column(Boolean)
    score_credito = Column(Float)
    saldo_cc = Column(Float)
