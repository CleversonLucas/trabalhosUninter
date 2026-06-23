from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.dependencies import get_usuario_logado
from app.schemas.produto_schema import ProdutoResponse
from app.services.produto_service import listar_produtos

router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)


@router.get("", response_model=List[ProdutoResponse])
def listar(
    db: Session = Depends(get_db),
    usuario=Depends(get_usuario_logado)
):
    return listar_produtos(db)