from decimal import Decimal

from app.core.database import SessionLocal, Base, engine
from app.models.usuario import Usuario
from app.models.unidade import Unidade
from app.models.produto import Produto
from app.models.estoque import Estoque
from app.core.security import gerar_hash_senha


def executar_seed():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        usuario_existente = db.query(Usuario).filter(
            Usuario.email == "cliente@raizes.com"
        ).first()

        if usuario_existente:
            print("Seed já executado anteriormente.")
            return

        cliente = Usuario(
            nome="Cliente Exemplo",
            email="cliente@raizes.com",
            senha_hash=gerar_hash_senha("123456"),
            perfil="CLIENTE",
            ativo=True
        )

        atendente = Usuario(
            nome="Atendente Exemplo",
            email="atendente@raizes.com",
            senha_hash=gerar_hash_senha("123456"),
            perfil="ATENDENTE",
            ativo=True
        )

        cozinha = Usuario(
            nome="Cozinha Exemplo",
            email="cozinha@raizes.com",
            senha_hash=gerar_hash_senha("123456"),
            perfil="COZINHA",
            ativo=True
        )

        gerente = Usuario(
            nome="Gerente Exemplo",
            email="gerente@raizes.com",
            senha_hash=gerar_hash_senha("123456"),
            perfil="GERENTE",
            ativo=True
        )

        admin = Usuario(
            nome="Administrador Exemplo",
            email="admin@raizes.com",
            senha_hash=gerar_hash_senha("123456"),
            perfil="ADMIN",
            ativo=True
        )

        unidade = Unidade(
            nome="Raízes do Nordeste - Recife Centro",
            cidade="Recife",
            ativa=True
        )

        produto1 = Produto(
            nome="Cuscuz com queijo coalho",
            descricao="Cuscuz nordestino servido com queijo coalho.",
            preco=Decimal("14.90"),
            ativo=True
        )

        produto2 = Produto(
            nome="Tapioca de carne seca",
            descricao="Tapioca recheada com carne seca e queijo.",
            preco=Decimal("18.90"),
            ativo=True
        )

        produto3 = Produto(
            nome="Suco de cajá",
            descricao="Suco regional natural.",
            preco=Decimal("8.50"),
            ativo=True
        )

        db.add_all([
            cliente,
            atendente,
            cozinha,
            gerente,
            admin,
            unidade,
            produto1,
            produto2,
            produto3
        ])

        db.commit()

        db.refresh(unidade)
        db.refresh(produto1)
        db.refresh(produto2)
        db.refresh(produto3)

        estoque1 = Estoque(
            produto_id=produto1.id,
            unidade_id=unidade.id,
            quantidade=20
        )

        estoque2 = Estoque(
            produto_id=produto2.id,
            unidade_id=unidade.id,
            quantidade=15
        )

        estoque3 = Estoque(
            produto_id=produto3.id,
            unidade_id=unidade.id,
            quantidade=30
        )

        db.add_all([estoque1, estoque2, estoque3])
        db.commit()

        print("Seed executado com sucesso.")

    finally:
        db.close()


if __name__ == "__main__":
    executar_seed()