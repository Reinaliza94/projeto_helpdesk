#Model chamados
from models.conexao import *
from sqlalchemy import Column, Integer, String, DateTime

class Chamados(Base):
 
    __tablename__ = "chamados"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    titulo = Column("titulo", String (200))
    descricao = Column("descricao", String (500))
    data_abertura = Column("data_abertura", DateTime)
    data_fechamento = Column("data_fechamento", DateTime)
    status = Column("status", String (20))
    prioridade = Column("prioridade", String (20))
    categoria = Column("categoria", String (100))
    id_usuario = Column("id_usuario", Integer)
    responsavel_tecnico = Column("responsavel_tecnico", String (200))

    def __init__(self, titulo, descricao, data_abertura, data_fechamento, status, prioridade, categoria, id_usuario, responsavel_tecnico):
        self.titulo = titulo
        self.descricao = descricao
        self.data_abertura = data_abertura
        self.data_fechamento = data_fechamento
        self.status = status
        self.prioridade = prioridade
        self.categoria = categoria
        self.id_usuario = id_usuario
        self.responsavel_tecnico = responsavel_tecnico
    
Base.metadata.create_all(bind=engine)