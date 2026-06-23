from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


class UsuarioTokenResponse(BaseModel):
    id: int
    nome: str
    email: str
    perfil: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioTokenResponse