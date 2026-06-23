from sqlalchemy.orm import Session
from app.repositories.produto_repository import listar_produtos_ativos


def listar_produtos(db: Session):
    return listar_produtos_ativos(db)