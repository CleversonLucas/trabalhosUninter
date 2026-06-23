from sqlalchemy.orm import Session

from app.models.estoque import Estoque


def buscar_estoque_por_produto_unidade(
    db: Session,
    produto_id: int,
    unidade_id: int
):
    return (
        db.query(Estoque)
        .filter(
            Estoque.produto_id == produto_id,
            Estoque.unidade_id == unidade_id
        )
        .first()
    )


def atualizar_estoque(db: Session, estoque: Estoque):
    db.add(estoque)
    db.flush()
    return estoque