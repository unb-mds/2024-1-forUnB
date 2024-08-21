# ForUnB - Configuração do Projeto

Esta pasta `forunb` contém os arquivos principais de configuração e gerenciamento do projeto **ForUnB**. Diferente dos apps tradicionais do Django, esta pasta não contém models, views ou templates, mas é essencial para o funcionamento geral do projeto.

## Descrição dos Arquivos
- **__init__.py:** Arquivo vazio que indica ao Python que este diretório deve ser tratado como um módulo.
- **asgi.py:** Configuração para a interface ASGI (Asynchronous Server Gateway Interface), usada para servir o projeto em um ambiente assíncrono.
- **settings/:** Diretório que contém os arquivos de configuração do projeto.
- **base.py:** Contém as configurações básicas e comuns a todos os ambientes.
- **production.py:** Configurações específicas para o ambiente de produção.
- **urls.py:** Define os roteamentos principais do projeto, conectando URLs a views.
- **wsgi.py:** Configuração para a interface WSGI (Web Server Gateway Interface), usada para servir o projeto em ambientes síncronos.

## Licença
Este projeto está licenciado sob os termos da licença MIT.

Esse `README.md` oferece uma visão geral da função da pasta `forunb` no projeto Django 'ForUnB', explicando a finalidade dos principais arquivos de configuração.