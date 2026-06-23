from datetime import datetime
from pydantic import BaseModel


class AuditoriaResponse(BaseModel):
    id: int
    usuario_id: int
    acao: str
    entidade: str
    registro_id: int
    detalhes: str | None
    data_hora: datetime

    class Config:
        from_attributes = True