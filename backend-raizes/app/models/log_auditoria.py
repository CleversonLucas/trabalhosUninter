from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class LogAuditoria(Base):
    __tablename__ = "logs_auditoria"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    acao = Column(String, nullable=False)
    entidade = Column(String, nullable=False)
    registro_id = Column(Integer, nullable=False)
    detalhes = Column(String, nullable=True)

    data_hora = Column(DateTime(timezone=True), server_default=func.now())