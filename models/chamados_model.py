# Model chamados
from sqlalchemy import Column, Integer, String, DateTime
from models.conexao import Base


class Chamados(Base):
    __tablename__ = "chamados"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200))
    descricao = Column(String(500))
    data_abertura = Column(DateTime)
    data_fechamento = Column(DateTime)
    status = Column(String(20))
    prioridade = Column(String(20))
    categoria = Column(String(100))
    id_usuario = Column(Integer)
    responsavel_tecnico = Column(String(200))

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