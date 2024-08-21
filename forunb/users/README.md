# Users App
## Descrição

Este é o app `Users` do projeto **ForUnB**. Ele gerencia as funcionalidades relacionadas a autenticação de usuários, como registro, login e perfil.

## Funcionalidades
- **Registro de Usuário:** Permite que novos usuários se registrem no sistema.
- **Login:** Permite que os usuários existentes façam login.
- **Perfil de Usuário:** Permite que os usuários visualizem e editem seus perfis.

## Descrição dos Arquivos
- **admin.py:** Configurações do painel administrativo do Django para gerenciar usuários.
- **apps.py:** Configurações do app Users.
- **forms.py:** Define formulários personalizados para registro e edição de perfis.
- **models.py:** Define os modelos relacionados aos usuários.
- **views.py:** Contém as views que tratam as requisições para registro, login, e perfil.
- **urls.py:** Contém as urls utilizadas no app Users.
- **templates/users/:** Contém os templates HTML para as páginas de login, registro e perfil.

## Como Usar:
### Registro
Para permitir que novos usuários se registrem, utilize a view de register. O template associado é o register.html e o register_unb_email.html.

### Login
Os usuários podem acessar o sistema através da view de login. O template utilizado é o login.html.

### Perfil
Os usuários podem visualizar e editar seus perfis através da view de profile, que utiliza o template profile.html.

## Testes:
Os testes automatizados para este app podem ser encontrados em tests. Execute-os com:
```bash
python manage.py test users
```

## Licença
Este projeto está licenciado sob os termos da licença MIT.

Esse arquivo `README.md` fornece uma visão geral do app `Users` e como ele se encaixa no projeto 'ForUnB'. Ele também inclui informações sobre estrutura e uso.