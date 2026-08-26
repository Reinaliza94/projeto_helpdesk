#Model usuarios
from models.conexao import *

class Usuarios(Base):
 
    __tablename__ = "usuarios"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String(200))
    email = Column("email", String(100))
    departamento = Column("departamento", String(200))
    ramal = Column("ramal", String(15))
    status = Column("status", String(15))

 #A funçao __init__ serve para inicializar a classe (construtor da classe)

    def __init__(self, nome, email, departamento, ramal, status):
        self.nome = nome
        self.email = email
        self.departamento = departamento
        self.ramal = ramal
        self.status = status

# Criando as tabelas no banco de dados (caso não existam)
Base.metadata.create_all(bind=engine)