from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    forma_pagamento = Column(String, nullable=False)
    status = Column(String, nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    transacao_externa = Column(String, nullable=True)

    data_criacao = Column(DateTime(timezone=True), server_default=func.now())