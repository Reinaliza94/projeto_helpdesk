#Model usuarios
from models.conexao import *
from sqlalchemy import Column, Integer, String

class Usuarios(Base):
 
    __tablename__ = "usuarios"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String(200))
    email = Column("email", String(50))
    departamento = Column("departamento", String(200))
    ramal = Column("ramal", String(15))
    status = Column("status", String(15))

    def __init__(self, nome, email, departamento, ramal, status):
        self.nome = nome
        self.email = email
        self.departamento = departamento
        self.ramal = ramal
        self.status = status

Base.metadata.create_all(bind=engine)