from sqlalchemy.orm import Session

from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido
from app.models.pagamento import Pagamento


def salvar_pedido(db: Session, pedido: Pedido):
    db.add(pedido)
    db.flush()
    return pedido


def salvar_item_pedido(db: Session, item: ItemPedido):
    db.add(item)
    db.flush()
    return item


def salvar_pagamento(db: Session, pagamento: Pagamento):
    db.add(pagamento)
    db.flush()
    return pagamento


def atualizar_pedido(db: Session, pedido: Pedido):
    db.add(pedido)
    db.flush()
    return pedido


def buscar_pedido_por_id(db: Session, pedido_id: int):
    return db.query(Pedido).filter(Pedido.id == pedido_id).first()


def listar_pedidos(
    db: Session,
    canal_pedido: str | None = None,
    status: str | None = None,
    cliente_id: int | None = None
):
    query = db.query(Pedido)

    if canal_pedido:
        query = query.filter(Pedido.canal_pedido == canal_pedido.upper())

    if status:
        query = query.filter(Pedido.status == status.upper())

    if cliente_id:
        query = query.filter(Pedido.cliente_id == cliente_id)

    return query.order_by(Pedido.id.desc()).all()