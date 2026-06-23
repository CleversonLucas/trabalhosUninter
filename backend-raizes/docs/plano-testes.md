# 11. Plano de Testes

## 11.1 Visão Geral

O plano de testes tem como objetivo validar o funcionamento da API desenvolvida para o sistema Raízes do Nordeste. Os testes foram definidos com foco no fluxo principal do projeto: autenticação, consulta de produtos, criação de pedido, validação de estoque, pagamento mock, atualização de status e auditoria.

Os cenários contemplam tanto situações esperadas, chamadas de testes positivos, quanto situações de erro, chamadas de testes negativos. Dessa forma, é possível verificar se a API responde corretamente em diferentes condições de uso.

## 11.2 Estratégia de Testes

Os testes serão executados por meio do Swagger/OpenAPI disponibilizado pelo FastAPI e também poderão ser reproduzidos em uma coleção Postman ou Insomnia.

A ordem sugerida para execução dos testes é:

1. Executar o seed inicial.
2. Realizar login com os usuários de teste.
3. Autorizar o token JWT no Swagger.
4. Consultar produtos.
5. Criar pedidos.
6. Atualizar status.
7. Consultar auditoria.
8. Executar cenários negativos.

## 11.3 Cenários de Teste

| ID  | Cenário                               | Endpoint                          | Pré-condição                                   | Entrada                                                       | Resultado esperado                                          | Evidência                                   |
| --- | ------------------------------------- | --------------------------------- | ---------------------------------------------- | ------------------------------------------------------------- | ----------------------------------------------------------- | ------------------------------------------- |
| T01 | Login válido                          | POST /auth/login                  | Usuário cadastrado pelo seed                   | E-mail e senha válidos                                        | Status 200 e retorno do token JWT                           | Swagger / Auth - Login válido               |
| T02 | Login inválido                        | POST /auth/login                  | Usuário cadastrado                             | Senha incorreta                                               | Status 401 e mensagem de credenciais inválidas              | Swagger / Auth - Login inválido             |
| T03 | Consultar produtos com token          | GET /produtos                     | Usuário autenticado                            | Token JWT válido                                              | Status 200 e lista de produtos ativos                       | Swagger / Produtos - Listar produtos        |
| T04 | Consultar produtos sem token          | GET /produtos                     | Nenhuma                                        | Sem token JWT                                                 | Status 401 e erro de autenticação                           | Swagger / Produtos - Sem token              |
| T05 | Criar pedido aprovado                 | POST /pedidos                     | Cliente autenticado e estoque disponível       | Pedido com canal APP, produto válido e forma de pagamento PIX | Status 201, pedido criado, pagamento APROVADO e status PAGO | Swagger / Pedidos - Pedido aprovado         |
| T06 | Criar pedido com pagamento negado     | POST /pedidos                     | Cliente autenticado e estoque disponível       | Pedido com forma_pagamento RECUSADO                           | Status 201, pagamento NEGADO e pedido CANCELADO             | Swagger / Pedidos - Pagamento negado        |
| T07 | Criar pedido com estoque insuficiente | POST /pedidos                     | Cliente autenticado                            | Quantidade maior que o estoque disponível                     | Status 409 e erro ESTOQUE_INSUFICIENTE                      | Swagger / Pedidos - Estoque insuficiente    |
| T08 | Criar pedido com canal inválido       | POST /pedidos                     | Cliente autenticado                            | canal_pedido com valor inválido                               | Status 422 e erro CANAL_PEDIDO_INVALIDO                     | Swagger / Pedidos - Canal inválido          |
| T09 | Atualizar status do pedido            | PATCH /pedidos/{pedido_id}/status | Usuário COZINHA autenticado e pedido existente | Novo status EM_PREPARO                                        | Status 200 e mensagem de status atualizado                  | Swagger / Pedidos - Atualizar status        |
| T10 | Atualizar status sem permissão        | PATCH /pedidos/{pedido_id}/status | Cliente autenticado                            | Tentativa de alterar status                                   | Status 403 e erro de acesso negado                          | Swagger / Pedidos - Sem permissão           |
| T11 | Consultar pedidos por canal           | GET /pedidos?canal_pedido=APP     | Usuário autenticado e pedidos cadastrados      | Filtro canal_pedido=APP                                       | Status 200 e lista filtrada por canal                       | Swagger / Pedidos - Filtro por canal        |
| T12 | Consultar auditoria como gerente      | GET /auditoria                    | Usuário GERENTE autenticado                    | Token JWT válido                                              | Status 200 e lista de logs de auditoria                     | Swagger / Auditoria - Listar logs           |
| T13 | Consultar auditoria como cliente      | GET /auditoria                    | Usuário CLIENTE autenticado                    | Token JWT válido                                              | Status 403 e erro de acesso negado                          | Swagger / Auditoria - Cliente sem permissão |

## 11.4 Cobertura dos Testes

Os testes definidos cobrem os principais pontos exigidos para a API:

* autenticação com JWT;
* acesso sem token;
* controle de permissão por perfil;
* listagem de produtos;
* criação de pedido;
* validação de estoque;
* registro do canal do pedido;
* pagamento mock aprovado;
* pagamento mock negado;
* atualização de status;
* consulta de auditoria;
* padronização de erros.

## 11.5 Considerações

Os testes foram planejados para demonstrar o funcionamento do fluxo principal da aplicação e também a resposta da API em situações de erro. Com isso, é possível validar tanto o comportamento esperado quanto as regras de segurança, permissão e negócio implementadas.
