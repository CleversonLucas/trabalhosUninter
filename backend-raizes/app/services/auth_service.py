from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.usuario_repository import buscar_usuario_por_email
from app.core.security import verificar_senha, criar_token_acesso


def autenticar_usuario(db: Session, email: str, senha: str):
    usuario = buscar_usuario_por_email(db, email)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "CREDENCIAIS_INVALIDAS",
                "message": "E-mail ou senha inválidos.",
                "details": []
            }
        )

    if not verificar_senha(senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "CREDENCIAIS_INVALIDAS",
                "message": "E-mail ou senha inválidos.",
                "details": []
            }
        )

    if not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "USUARIO_INATIVO",
                "message": "Usuário inativo no sistema.",
                "details": []
            }
        )

    token = criar_token_acesso(
        data={
            "sub": str(usuario.id),
            "email": usuario.email,
            "perfil": usuario.perfil
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "perfil": usuario.perfil
        }
    }