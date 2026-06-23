# API Raízes do Nordeste

API Back-end desenvolvida para o projeto multidisciplinar da trilha Back-end. O sistema simula o funcionamento de uma rede de lanchonetes, permitindo autenticação de usuários, consulta de produtos, criação de pedidos, validação de estoque, pagamento mock, atualização de status e auditoria.

## 1. Tecnologias Utilizadas

* Python
* FastAPI
* SQLAlchemy
* SQLite
* JWT
* Passlib / Bcrypt
* Swagger / OpenAPI
* Pytest

## 2. Objetivo da API

O objetivo da API é demonstrar um fluxo funcional de pedidos para a rede Raízes do Nordeste.

O fluxo principal implementado é:

1. Usuário realiza login.
2. Usuário consulta produtos disponíveis.
3. Usuário cria um pedido informando unidade, canal do pedido, itens e forma de pagamento.
4. O sistema valida o estoque.
5. O sistema registra o pedido.
6. O sistema simula o pagamento.
7. O sistema atualiza o status do pedido.
8. O sistema registra logs de auditoria.

## 3. Estrutura do Projeto

backend-raizes/
app/
api/
routes/
core/
exceptions/
models/
repositories/
schemas/
seed/
services/
tests/
docs/
requirements.txt
.env.example
README.md

## 4. Como Executar o Projeto

### 4.1 Criar ambiente virtual

```bash
python -m venv venv
```

### 4.2 Ativar ambiente virtual

No Windows:

```bash
venv\Scripts\activate
```

No Linux/Mac:

```bash
source venv/bin/activate
```

### 4.3 Instalar dependências

```bash
pip install -r requirements.txt
```

### 4.4 Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
DATABASE_URL=sqlite:///./raizes.db
SECRET_KEY=chave-secreta-projeto-raizes
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 4.5 Executar o seed inicial

O seed cria usuários, unidade, produtos e estoque inicial.

```bash
python -m app.seed.seed_data
```

Resultado esperado:

```text
Seed executado com sucesso.
```

Caso o seed já tenha sido executado:

```text
Seed já executado anteriormente.
```

### 4.6 Iniciar a API

```bash
uvicorn app.main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

A documentação Swagger ficará disponível em:

```text
http://127.0.0.1:8000/docs
```

## 5. Usuários de Teste

Todos os usuários criados pelo seed possuem a senha:

```text
123456
```

| Perfil    | E-mail                                              |
| --------- | --------------------------------------------------- |
| CLIENTE   | [cliente@raizes.com](mailto:cliente@raizes.com)     |
| ATENDENTE | [atendente@raizes.com](mailto:atendente@raizes.com) |
| COZINHA   | [cozinha@raizes.com](mailto:cozinha@raizes.com)     |
| GERENTE   | [gerente@raizes.com](mailto:gerente@raizes.com)     |
| ADMIN     | [admin@raizes.com](mailto:admin@raizes.com)         |

## 6. Endpoints Principais

### Autenticação

```text
POST /auth/login
```

Realiza login e retorna token JWT.

### Produtos

```text
GET /produtos
```

Lista produtos ativos cadastrados.

### Pedidos

```text
POST /pedidos
GET /pedidos
GET /pedidos/{pedido_id}
PATCH /pedidos/{pedido_id}/status
```

Permite criar, consultar, filtrar e atualizar pedidos.

### Auditoria

```text
GET /auditoria
```

Lista registros de ações importantes do sistema. Disponível apenas para GERENTE e ADMIN.

## 7. Como Testar o Fluxo Principal no Swagger

### 7.1 Login

Acesse:

```text
POST /auth/login
```

Use o corpo:

```json
{
  "email": "cliente@raizes.com",
  "senha": "123456"
}
```

Copie o valor retornado em `access_token`.

### 7.2 Autorizar no Swagger

Clique no botão `Authorize` no topo da página do Swagger.

Cole o token JWT no campo solicitado e confirme.

### 7.3 Consultar Produtos

Execute:

```text
GET /produtos
```

### 7.4 Criar Pedido com Pagamento Aprovado

Execute:

```text
POST /pedidos
```

Corpo da requisição:

```json
{
  "unidade_id": 1,
  "canal_pedido": "APP",
  "itens": [
    {
      "produto_id": 1,
      "quantidade": 2
    }
  ],
  "forma_pagamento": "PIX"
}
```

Resultado esperado:

* pedido criado;
* estoque validado;
* pagamento aprovado;
* status final do pedido como `PAGO`.

### 7.5 Criar Pedido com Pagamento Negado

Execute:

```text
POST /pedidos
```

Corpo da requisição:

```json
{
  "unidade_id": 1,
  "canal_pedido": "TOTEM",
  "itens": [
    {
      "produto_id": 2,
      "quantidade": 1
    }
  ],
  "forma_pagamento": "RECUSADO"
}
```

Resultado esperado:

* pagamento mock negado;
* pedido com status `CANCELADO`.

### 7.6 Atualizar Status do Pedido

Faça login com o usuário da cozinha:

```json
{
  "email": "cozinha@raizes.com",
  "senha": "123456"
}
```

Autorize no Swagger com o novo token.

Execute:

```text
PATCH /pedidos/{pedido_id}/status
```

Exemplo de corpo:

```json
{
  "status": "EM_PREPARO"
}
```

### 7.7 Consultar Auditoria

Faça login como gerente:

```json
{
  "email": "gerente@raizes.com",
  "senha": "123456"
}
```

Execute:

```text
GET /auditoria
```

Resultado esperado:

* registros de pedido criado;
* pagamento aprovado ou negado;
* alteração de status.

## 8. Testes Negativos Sugeridos

### Token ausente

Executar `GET /produtos` sem autenticação.

Resultado esperado:

```text
401 Unauthorized
```

### Perfil sem permissão

Executar `GET /auditoria` com usuário CLIENTE.

Resultado esperado:

```text
403 Forbidden
```

### Estoque insuficiente

Criar pedido com quantidade muito alta.

Resultado esperado:

```text
409 Conflict
```

### Canal inválido

Criar pedido com canal inexistente.

Resultado esperado:

```text
422 Unprocessable Entity
```

## 9. Observações

A integração de pagamento é simulada por meio de um serviço mock. Não existe integração com provedor real de pagamento.

Para facilitar os testes:

* `forma_pagamento = "RECUSADO"` retorna pagamento negado;
* qualquer outro valor retorna pagamento aprovado.

## 10. Autor

Projeto desenvolvido para fins acadêmicos na disciplina de Projeto Multidisciplinar — Trilha Back-end.
