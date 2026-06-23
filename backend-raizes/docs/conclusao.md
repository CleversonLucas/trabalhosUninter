# 13. Conclusão

O projeto desenvolvido teve como objetivo propor e implementar uma solução Back-end para a rede Raízes do Nordeste, considerando o cenário de crescimento da empresa, múltiplos canais de atendimento e necessidade de maior controle sobre pedidos, estoque, pagamento e auditoria.

A solução foi desenvolvida como uma API REST utilizando Python com FastAPI. A escolha dessa tecnologia permitiu criar uma aplicação objetiva, documentada automaticamente pelo Swagger/OpenAPI e adequada para testes e validação dos endpoints.

O fluxo principal implementado foi o processo de criação de pedido com pagamento simulado. Esse fluxo contempla a autenticação do usuário, a validação dos dados recebidos, a verificação de estoque, o registro do pedido, o processamento do pagamento mock, a atualização do status do pedido e o registro das ações em auditoria.

Durante o desenvolvimento, foram considerados requisitos importantes do estudo de caso, como multicanalidade, controle de estoque por unidade, integração com serviço externo de pagamento simulado, segurança, controle de acesso por perfil e cuidados básicos relacionados à LGPD.

A modelagem do sistema foi representada por meio de diagramas, como o DER, o diagrama de casos de uso, o diagrama de classes e o fluxo crítico do pedido. Esses artefatos ajudaram a manter coerência entre a análise do problema, a estrutura do banco de dados, os endpoints da API e a implementação realizada.

A API implementada possui autenticação com JWT, senhas protegidas por hash, controle de permissões por perfil, persistência em banco de dados, padrão de erro, seed inicial, documentação Swagger e coleção Postman para reprodução dos testes. Esses elementos tornam a entrega mais organizada e facilitam a validação por parte do avaliador.

Algumas funcionalidades foram deixadas como evolução futura, como programa completo de fidelidade, campanhas promocionais, relatórios gerenciais mais detalhados, dashboard administrativo e integração real com meios de pagamento. Essas funcionalidades não foram implementadas neste MVP para manter o foco no fluxo principal exigido pela trilha Back-end.

Conclui-se que a solução proposta atende ao objetivo do projeto, pois apresenta uma API funcional, documentada, testável e alinhada ao estudo de caso. Além disso, a organização em camadas, os testes planejados e os cuidados com segurança e auditoria demonstram uma preocupação com boas práticas de desenvolvimento e com a construção de uma solução que poderia evoluir para um ambiente real.
