from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.dependencies import get_usuario_logado, exigir_perfis
from app.schemas.pedido_schema import (
    PedidoCreateRequest,
    PedidoCreateResponse,
    PedidoResumoResponse,
    PedidoStatusUpdateRequest,
    PedidoStatusUpdateResponse
)
from app.services.pedido_service import (
    criar_pedido,
    consultar_pedidos,
    consultar_pedido_por_id,
    atualizar_status_pedido
)

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


@router.post("", response_model=PedidoCreateResponse, status_code=201)
def criar(
    dados: PedidoCreateRequest,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_perfis(["CLIENTE", "ATENDENTE"]))
):
    return criar_pedido(db, dados, usuario)


@router.get("", response_model=List[PedidoResumoResponse])
def listar(
    canal_pedido: str | None = Query(default=None),
    status: str | None = Query(default=None),
    db: Session = Depends(get_db),
    usuario=Depends(get_usuario_logado)
):
    return consultar_pedidos(
        db=db,
        usuario=usuario,
        canal_pedido=canal_pedido,
        status_pedido=status
    )


@router.get("/{pedido_id}", response_model=PedidoResumoResponse)
def buscar_por_id(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_usuario_logado)
):
    return consultar_pedido_por_id(db, pedido_id, usuario)


@router.patch("/{pedido_id}/status", response_model=PedidoStatusUpdateResponse)
def atualizar_status(
    pedido_id: int,
    dados: PedidoStatusUpdateRequest,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_perfis(["ATENDENTE", "COZINHA", "GERENTE", "ADMIN"]))
):
    return atualizar_status_pedido(
        db=db,
        pedido_id=pedido_id,
        novo_status=dados.status,
        usuario=usuario
    )