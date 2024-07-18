# Git Flow

## Introdução

O Git Flow é um modelo de ramificação para o Git, criado por Vincent Driessen, que oferece uma estratégia robusta para gerenciar as branches (ramificações) de um projeto. Este modelo facilita o desenvolvimento paralelo, a liberação de versões e a manutenção de múltiplas versões de produção.

## Estrutura do Git Flow

O Git Flow define um conjunto de branches e regras para gerenciar e interagir com elas. As principais branches são:

- **Main**: Contém o histórico oficial do projeto. As releases são extraídas desta branch.
- **Develop**: Serve como a branch de integração para as features. O código nesta branch deve estar pronto para ser liberado na próxima release.

### Branches de Suporte

- **Feature**: Usada para desenvolver novas funcionalidades para o próximo release. São criadas a partir da `develop` e, uma vez concluídas, são fundidas de volta na `develop`.
- **Release**: Suporta a preparação de uma nova release de produção. Permite pequenas correções e testes. É criada a partir da `develop` e fundida em `main` e `develop`.
- **Hotfix**: Usada para corrigir rapidamente bugs em produção. Criada a partir da `main` e, uma vez concluída, é fundida em `main` e `develop`.

## Fluxo de Trabalho do Git Flow


Para iniciar o fluxo de desenvolvimento das atividades, é fundamental entender os conceitos de **issue** e **pull request**.

- **Issue**: É a forma de descrever os problemas e tarefas que serão abordados durante a sprint, incluindo eventuais problemas no código. As issues ajudam a organizar e priorizar o trabalho, garantindo que todos saibam o que precisa ser feito.

- **Pull Request**: É o método utilizado para gerenciar e integrar branches do código sem interferir no trabalho de outros desenvolvedores. Os pull requests permitem revisar e discutir mudanças antes de mesclá-las, facilitando o desenvolvimento paralelo e mantendo a qualidade do código.
