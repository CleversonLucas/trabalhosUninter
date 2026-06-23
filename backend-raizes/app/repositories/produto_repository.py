from sqlalchemy.orm import Session
from app.models.produto import Produto


def listar_produtos_ativos(db: Session):
    return db.query(Produto).filter(Produto.ativo == True).all()


def buscar_produto_por_id(db: Session, produto_id: int):
    return db.query(Produto).filter(Produto.id == produto_id).first()