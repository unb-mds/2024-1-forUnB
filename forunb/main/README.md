# Main App

## Descrição
Este é o app `Main` do projeto **ForUnB**. Ele gerencia as principais funcionalidades do site, incluindo a página inicial, visualização de fóruns, interação com perguntas e respostas, notificações, e muito mais.

## Funcionalidades
- **Página Inicial (index):** Exibe uma visão geral dos fóruns disponíveis e outras informações relevantes.
- **Visualização de Fórum (forum_detail):** Mostra detalhes de um fórum específico, incluindo suas perguntas e discussões.
- **Lista de Fóruns (forum_list):** Exibe uma lista de todos os fóruns disponíveis na plataforma.
- **Fóruns Seguidos (followed_forums):** Exibe os fóruns que o usuário segue.
- **Perguntas (questions):** Exibe uma lista de perguntas dentro de um fórum específico.
- **Postagens do Usuário (user_posts):** Mostra todas as postagens feitas por um usuário, incluindo perguntas e respostas.
- **Detalhes da Pergunta (question_detail):** Exibe detalhes de uma pergunta específica.
- **Seguir Fórum (follow_forum):** Permite que o usuário siga ou deixe de seguir um fórum.
- **Nova Pergunta (new_question):** Permite que o usuário crie uma nova pergunta em um fórum.
- **Nova Resposta (new_answer):** Permite que o usuário responda a uma pergunta existente.
- **Deletar Pergunta (delete_question):** Permite que o autor de uma pergunta a exclua.
- **Deletar Resposta (delete_answer):** Permite que o autor de uma resposta a exclua.
- **Notificações (notifications):** Exibe notificações para o usuário sobre atividades relevantes.
- **Upvote:** Permite que o usuário dê upvotes em perguntas e respostas.
- **Reportar Conteúdo (report):** Permite que o usuário denuncie conteúdo inapropriado.

## Descrição dos Arquivos
- **admin.py:** Configurações do painel administrativo do Django para gerenciar fóruns, perguntas e respostas.
- **apps.py:** Configurações do app Main.
- **forms.py:** Define os formulários usados para criar e editar perguntas, respostas e outras interações.
- **models.py:** Define os modelos de dados para fóruns, perguntas, respostas, etc.
- **views.py:** Contém as views que tratam das requisições e renderizam os templates apropriados.
- **urls.py:** Contém as urls utilizadas no app Main.
- **templates/main/:** Contém os templates HTML para as páginas principais do site.
- **scraping.py:** Tem um read.me detalhado sobre este arquivo dentro da pasta main/management.

## Como Usar
### Páginas Principais:
- **Página Inicial:** A página inicial do site, carregada através da view index, está associada ao template index.html.
- **Visualização de Fórum:** A view forum_detail renderiza a página de detalhes de um fórum utilizando o template forum_detail.html.
- **Lista de Fóruns:** A lista de todos os fóruns disponíveis é renderizada pela view forum_list utilizando o template forums.html.

### Interação com Fóruns e Perguntas:
- **Seguir Fóruns:** A view follow_forum permite que o usuário siga ou deixe de seguir um fórum.
- **Nova Pergunta:** A view new_question permite que o usuário crie uma nova pergunta, utilizando o template new_question.html.
- **Nova Resposta:** A view new_answer permite que o usuário adicione uma resposta a uma pergunta, utilizando o template new_answer.html.

### Gerenciamento de Conteúdo:
- **Deletar Pergunta e Resposta:** As views delete_question e delete_answer permitem que o autor exclua sua pergunta ou resposta.
- **Upvotes e Denúncias:** As funcionalidades de upvote e reportar conteúdo são gerenciadas por views específicas que tratam essas interações.

### Notificações:
- **Notificações:** A view notifications exibe as notificações do usuário, renderizando o template notifications.html.

## Testes:
Os testes automatizados para este app estão em tests. Execute-os com:
```bash
python manage.py test main
```

## Licença
Este projeto está licenciado sob os termos da licença MIT.

Este `README.md` fornece uma visão detalhada das funcionalidades do app `Main`, explicando como cada parte se integra no projeto 'ForUnB'.