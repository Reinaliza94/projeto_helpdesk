from sqlalchemy import Column, Integer, String
from models.conexao import Base


class Tecnicos(Base):
    __tablename__ = "tecnicos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100))
    email = Column(String(50))
    departamento = Column(String(100))
    ramal = Column(String(15))
    status = Column(String(15))

    def __init__(self, nome, email, departamento, ramal, status):
        self.nome = nome
        self.email = email
        self.departamento = departamento
        self.ramal = ramal
        self.status = status