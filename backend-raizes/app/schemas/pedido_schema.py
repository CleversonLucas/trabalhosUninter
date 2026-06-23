from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field


class ItemPedidoRequest(BaseModel):
    produto_id: int
    quantidade: int = Field(gt=0)


class PedidoCreateRequest(BaseModel):
    unidade_id: int
    canal_pedido: str
    itens: List[ItemPedidoRequest]
    forma_pagamento: str


class ItemPedidoResponse(BaseModel):
    produto_id: int
    quantidade: int
    preco_unitario: Decimal
    subtotal: Decimal

    class Config:
        from_attributes = True


class PagamentoPedidoResponse(BaseModel):
    status: str
    forma_pagamento: str
    valor: Decimal

    class Config:
        from_attributes = True


class PedidoCreateResponse(BaseModel):
    id: int
    cliente_id: int
    unidade_id: int
    canal_pedido: str
    status: str
    valor_total: Decimal
    itens: List[ItemPedidoResponse]
    pagamento: PagamentoPedidoResponse

    class Config:
        from_attributes = True


class PedidoResumoResponse(BaseModel):
    id: int
    cliente_id: int
    unidade_id: int
    canal_pedido: str
    status: str
    valor_total: Decimal

    class Config:
        from_attributes = True


class PedidoStatusUpdateRequest(BaseModel):
    status: str


class PedidoStatusUpdateResponse(BaseModel):
    id: int
    status: str
    message: str