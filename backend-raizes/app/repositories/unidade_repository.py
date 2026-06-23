from sqlalchemy.orm import Session

from app.models.unidade import Unidade


def buscar_unidade_por_id(db: Session, unidade_id: int):
    return db.query(Unidade).filter(Unidade.id == unidade_id).first()