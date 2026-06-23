# 12. Entrega Técnica

## 12.1 Visão Geral

A entrega técnica do projeto consiste em uma API Back-end funcional, desenvolvida em Python com FastAPI, com persistência em banco de dados, autenticação JWT, controle de permissões, documentação Swagger/OpenAPI e coleção de testes no Postman.

A solução implementa o fluxo principal definido para o MVP:

Pedido → Pagamento Mock → Atualização de Status → Auditoria

Esse fluxo permite demonstrar o funcionamento integrado entre autenticação, produtos, estoque, pedidos, pagamento simulado e registros de auditoria.

## 12.2 Repositório

O código-fonte do projeto será disponibilizado em um repositório público.

Link do repositório:

[INSERIR LINK DO GITHUB AQUI]

O repositório contém:

* código-fonte da API;
* estrutura organizada por camadas;
* arquivo README com instruções de execução;
* arquivo `.env.example`;
* seed inicial;
* coleção Postman;
* documentação complementar;
* imagens e diagramas utilizados no trabalho.

## 12.3 Estrutura Técnica do Projeto

A estrutura principal do projeto foi organizada da seguinte forma:

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
docs/
postman/
tests/
requirements.txt
.env.example
README.md

Essa organização separa as responsabilidades da aplicação, facilitando a manutenção e a evolução futura do projeto.

## 12.4 Execução da API

Para executar o projeto, é necessário instalar as dependências, configurar as variáveis de ambiente, executar o seed inicial e iniciar a API.

Comandos principais:

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

```bash
python -m app.seed.seed_data
```

```bash
uvicorn app.main:app --reload
```

Após iniciar a aplicação, a API fica disponível no endereço:

http://127.0.0.1:8000

## 12.5 Documentação Swagger/OpenAPI

A documentação da API é disponibilizada automaticamente pelo FastAPI.

Endereço local do Swagger:

http://127.0.0.1:8000/docs

Por meio do Swagger é possível visualizar e testar os endpoints implementados, como login, listagem de produtos, criação de pedidos, atualização de status e consulta de auditoria.

## 12.6 Coleção Postman

A coleção Postman foi criada para permitir a reprodução dos testes da API.

Local da coleção no repositório:

docs/postman/raizes-nordeste.postman_collection.json

A coleção contém requisições organizadas por módulos:

* Auth;
* Produtos;
* Pedidos;
* Auditoria.

Ela permite testar cenários positivos e negativos, incluindo autenticação, acesso sem token, criação de pedido, pagamento aprovado, pagamento negado, estoque insuficiente, atualização de status e controle de permissão.

## 12.7 Seed Inicial

O projeto possui um seed inicial responsável por cadastrar dados básicos para teste, incluindo:

* usuários com diferentes perfis;
* uma unidade da rede;
* produtos;
* estoque inicial.

Usuários criados pelo seed:

| Perfil    | E-mail                                              | Senha  |
| --------- | --------------------------------------------------- | ------ |
| CLIENTE   | [cliente@raizes.com](mailto:cliente@raizes.com)     | 123456 |
| ATENDENTE | [atendente@raizes.com](mailto:atendente@raizes.com) | 123456 |
| COZINHA   | [cozinha@raizes.com](mailto:cozinha@raizes.com)     | 123456 |
| GERENTE   | [gerente@raizes.com](mailto:gerente@raizes.com)     | 123456 |
| ADMIN     | [admin@raizes.com](mailto:admin@raizes.com)         | 123456 |

## 12.8 Fluxo Principal Implementado

O fluxo principal implementado permite que um cliente autenticado crie um pedido informando a unidade, o canal de origem, os itens desejados e a forma de pagamento.

Durante esse processo, o sistema:

1. valida o token do usuário;
2. verifica se o canal do pedido é válido;
3. verifica se a unidade existe;
4. verifica se os produtos existem;
5. valida se há estoque suficiente;
6. registra o pedido;
7. registra os itens do pedido;
8. processa o pagamento mock;
9. atualiza o status do pedido;
10. registra eventos de auditoria.

## 12.9 Evidências

As evidências da execução serão apresentadas por meio de:

* Swagger funcionando;
* prints dos endpoints testados;
* coleção Postman no repositório;
* README com instruções de execução;
* retorno da API nos principais cenários de teste.