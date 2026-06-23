from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido
from app.models.pagamento import Pagamento
from app.repositories.produto_repository import buscar_produto_por_id
from app.repositories.unidade_repository import buscar_unidade_por_id
from app.repositories.estoque_repository import (
    buscar_estoque_por_produto_unidade,
    atualizar_estoque
)
from app.repositories.pedido_repository import (
    salvar_pedido,
    salvar_item_pedido,
    salvar_pagamento,
    atualizar_pedido
)
from app.services.pagamento_service import processar_pagamento_mock
from app.services.auditoria_service import registrar_auditoria


CANAIS_VALIDOS = ["APP", "WEB", "TOTEM", "BALCAO", "PICKUP"]


def criar_pedido(db: Session, dados, usuario):
    if dados.canal_pedido.upper() not in CANAIS_VALIDOS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "CANAL_PEDIDO_INVALIDO",
                "message": "Canal do pedido inválido.",
                "details": [
                    {
                        "field": "canal_pedido",
                        "issue": "Valores aceitos: APP, WEB, TOTEM, BALCAO, PICKUP."
                    }
                ]
            }
        )

    if not dados.itens:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "PEDIDO_SEM_ITENS",
                "message": "O pedido deve possuir pelo menos um item.",
                "details": []
            }
        )

    unidade = buscar_unidade_por_id(db, dados.unidade_id)

    if not unidade or not unidade.ativa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "UNIDADE_NAO_ENCONTRADA",
                "message": "Unidade não encontrada ou inativa.",
                "details": []
            }
        )

    valor_total = Decimal("0.00")
    itens_processados = []

    for item in dados.itens:
        produto = buscar_produto_por_id(db, item.produto_id)

        if not produto or not produto.ativo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "PRODUTO_NAO_ENCONTRADO",
                    "message": f"Produto {item.produto_id} não encontrado ou inativo.",
                    "details": []
                }
            )

        estoque = buscar_estoque_por_produto_unidade(
            db,
            item.produto_id,
            dados.unidade_id
        )

        if not estoque or estoque.quantidade < item.quantidade:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": "ESTOQUE_INSUFICIENTE",
                    "message": "Não há quantidade suficiente para um ou mais produtos.",
                    "details": [
                        {
                            "field": f"produto_id={item.produto_id}",
                            "issue": f"Estoque disponível: {estoque.quantidade if estoque else 0}"
                        }
                    ]
                }
            )

        subtotal = Decimal(produto.preco) * item.quantidade
        valor_total += subtotal

        itens_processados.append({
            "produto": produto,
            "estoque": estoque,
            "quantidade": item.quantidade,
            "preco_unitario": Decimal(produto.preco),
            "subtotal": subtotal
        })

    pedido = Pedido(
        cliente_id=usuario.id,
        unidade_id=dados.unidade_id,
        canal_pedido=dados.canal_pedido.upper(),
        status="AGUARDANDO_PAGAMENTO",
        valor_total=valor_total
    )

    salvar_pedido(db, pedido)

    itens_resposta = []

    for item in itens_processados:
        item_pedido = ItemPedido(
            pedido_id=pedido.id,
            produto_id=item["produto"].id,
            quantidade=item["quantidade"],
            preco_unitario=item["preco_unitario"],
            subtotal=item["subtotal"]
        )

        salvar_item_pedido(db, item_pedido)

        item["estoque"].quantidade -= item["quantidade"]
        atualizar_estoque(db, item["estoque"])

        itens_resposta.append({
            "produto_id": item["produto"].id,
            "quantidade": item["quantidade"],
            "preco_unitario": item["preco_unitario"],
            "subtotal": item["subtotal"]
        })

    resultado_pagamento = processar_pagamento_mock(
        pedido_id=pedido.id,
        forma_pagamento=dados.forma_pagamento,
        valor=valor_total
    )

    pagamento = Pagamento(
        pedido_id=pedido.id,
        forma_pagamento=resultado_pagamento["forma_pagamento"],
        status=resultado_pagamento["status"],
        valor=resultado_pagamento["valor"],
        transacao_externa=resultado_pagamento["transacao_externa"]
    )

    salvar_pagamento(db, pagamento)

    if resultado_pagamento["status"] == "APROVADO":
        pedido.status = "PAGO"
        acao = "PAGAMENTO_APROVADO"
    else:
        pedido.status = "CANCELADO"
        acao = "PAGAMENTO_NEGADO"

    atualizar_pedido(db, pedido)

    registrar_auditoria(
        db=db,
        usuario_id=usuario.id,
        acao="PEDIDO_CRIADO",
        entidade="Pedido",
        registro_id=pedido.id,
        detalhes=f"Pedido criado pelo canal {pedido.canal_pedido}."
    )

    registrar_auditoria(
        db=db,
        usuario_id=usuario.id,
        acao=acao,
        entidade="Pagamento",
        registro_id=pagamento.id,
        detalhes=f"Pagamento mock retornou status {resultado_pagamento['status']}."
    )

    db.commit()

    return {
        "id": pedido.id,
        "cliente_id": pedido.cliente_id,
        "unidade_id": pedido.unidade_id,
        "canal_pedido": pedido.canal_pedido,
        "status": pedido.status,
        "valor_total": pedido.valor_total,
        "itens": itens_resposta,
        "pagamento": {
            "status": pagamento.status,
            "forma_pagamento": pagamento.forma_pagamento,
            "valor": pagamento.valor
        }
    }

from app.repositories.pedido_repository import buscar_pedido_por_id, listar_pedidos


STATUS_VALIDOS = [
    "AGUARDANDO_PAGAMENTO",
    "PAGO",
    "EM_PREPARO",
    "PRONTO",
    "ENTREGUE",
    "CANCELADO"
]


def consultar_pedidos(
    db: Session,
    usuario,
    canal_pedido: str | None = None,
    status_pedido: str | None = None
):
    cliente_id = None

    if usuario.perfil == "CLIENTE":
        cliente_id = usuario.id

    return listar_pedidos(
        db=db,
        canal_pedido=canal_pedido,
        status=status_pedido,
        cliente_id=cliente_id
    )


def consultar_pedido_por_id(db: Session, pedido_id: int, usuario):
    pedido = buscar_pedido_por_id(db, pedido_id)

    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "PEDIDO_NAO_ENCONTRADO",
                "message": "Pedido não encontrado.",
                "details": []
            }
        )

    if usuario.perfil == "CLIENTE" and pedido.cliente_id != usuario.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "ACESSO_NEGADO",
                "message": "Cliente só pode consultar seus próprios pedidos.",
                "details": []
            }
        )

    return pedido


def atualizar_status_pedido(
    db: Session,
    pedido_id: int,
    novo_status: str,
    usuario
):
    pedido = buscar_pedido_por_id(db, pedido_id)

    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "PEDIDO_NAO_ENCONTRADO",
                "message": "Pedido não encontrado.",
                "details": []
            }
        )

    novo_status = novo_status.upper()

    if novo_status not in STATUS_VALIDOS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "STATUS_INVALIDO",
                "message": "Status informado é inválido.",
                "details": [
                    {
                        "field": "status",
                        "issue": "Valores aceitos: AGUARDANDO_PAGAMENTO, PAGO, EM_PREPARO, PRONTO, ENTREGUE, CANCELADO."
                    }
                ]
            }
        )

    if pedido.status == "CANCELADO":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "PEDIDO_CANCELADO",
                "message": "Não é possível alterar o status de um pedido cancelado.",
                "details": []
            }
        )

    if pedido.status == "ENTREGUE":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "PEDIDO_ENTREGUE",
                "message": "Não é possível alterar o status de um pedido já entregue.",
                "details": []
            }
        )

    status_anterior = pedido.status
    pedido.status = novo_status

    atualizar_pedido(db, pedido)

    registrar_auditoria(
        db=db,
        usuario_id=usuario.id,
        acao="STATUS_PEDIDO_ALTERADO",
        entidade="Pedido",
        registro_id=pedido.id,
        detalhes=f"Status alterado de {status_anterior} para {novo_status}."
    )

    db.commit()

    return {
        "id": pedido.id,
        "status": pedido.status,
        "message": "Status do pedido atualizado com sucesso."
    }