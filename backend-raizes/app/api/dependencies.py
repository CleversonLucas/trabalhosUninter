from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import SECRET_KEY, ALGORITHM
from app.repositories.usuario_repository import buscar_usuario_por_id

security = HTTPBearer()


def get_usuario_logado(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = payload.get("sub")

        if usuario_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "error": "TOKEN_INVALIDO",
                    "message": "Token inválido ou sem identificação do usuário.",
                    "details": []
                }
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "TOKEN_INVALIDO",
                "message": "Token inválido ou expirado.",
                "details": []
            }
        )

    usuario = buscar_usuario_por_id(db, int(usuario_id))

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "USUARIO_NAO_ENCONTRADO",
                "message": "Usuário do token não foi encontrado.",
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

    return usuario


def exigir_perfis(perfis_permitidos: list[str]):
    def verificar_perfil(usuario=Depends(get_usuario_logado)):
        if usuario.perfil not in perfis_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "ACESSO_NEGADO",
                    "message": "Usuário não possui permissão para acessar este recurso.",
                    "details": []
                }
            )

        return usuario

    return verificar_perfil