import uuid
from decimal import Decimal


def processar_pagamento_mock(
    pedido_id: int,
    forma_pagamento: str,
    valor: Decimal
):
    """
    Simulação simples de pagamento.
    Para facilitar os testes:
    - forma_pagamento = "RECUSADO" retorna NEGADO
    - qualquer outra forma retorna APROVADO
    """

    if forma_pagamento.upper() == "RECUSADO":
        return {
            "pedido_id": pedido_id,
            "status": "NEGADO",
            "forma_pagamento": forma_pagamento,
            "valor": valor,
            "transacao_externa": f"mock-{uuid.uuid4()}"
        }

    return {
        "pedido_id": pedido_id,
        "status": "APROVADO",
        "forma_pagamento": forma_pagamento,
        "valor": valor,
        "transacao_externa": f"mock-{uuid.uuid4()}"
    }