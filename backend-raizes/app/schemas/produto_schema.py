from decimal import Decimal
from pydantic import BaseModel


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: str | None
    preco: Decimal
    ativo: bool

    class Config:
        from_attributes = True