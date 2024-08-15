# Descrição do funcionamento dos workflows
Os workflows são arquivos de configuração que definem um conjunto de ações que devem ser executadas em resposta a eventos específicos. Eles são compostos por jobs, que são executados em paralelo, e por steps, que são executados sequencialmente. Cada step é composto por uma ou mais ações, que são executadas em um ambiente específico. Dessa forma, separamos em 4 workflows:
    
- **CI**: responsável por executar os testes automatizados e garantir a qualidade do código.
- **docs**: responsável por gerar a documentação do projeto.
- **pylint**: responsável por executar o linting do código.
- **sonar**: responsável por enviar as métricas de qualidade do código para o SonarCloud.

## CI

Este fluxo de trabalho do GitHub Actions é acionado em eventos de push para o branch `main` e pull requests. Ele consiste em um único job chamado `u-tests` que é executado na versão mais recente do Ubuntu.

### Job: u-tests

O job `u-tests` usa uma matriz de estratégia para especificar a versão do Python a ser usada. Neste caso, está definido como `3.10`.

### Steps

1. **Checkout projeto**: Esta etapa faz o checkout do repositório usando a ação `actions/checkout`.

2. **Configurar Python**: Esta etapa configura a versão especificada do Python usando a ação `actions/setup-python`.

3. **Cache pip**: Esta etapa armazena em cache as dependências do pip usando a ação `actions/cache`. A chave de cache é gerada com base no sistema operacional e no hash do arquivo `requirements.txt`.

4. **Instalar dependências**: Esta etapa instala as dependências do projeto executando o comando `pip install`.

5. **Configurar ambiente**: Esta etapa configura o ambiente executando o comando `make config`.

6. **Testes**: Esta etapa executa os testes usando o comando `python ./forunb/manage.py test forunb`.


## Docs Deploy

Este fluxo de trabalho do GitHub Actions é acionado em eventos de push para o branch `main` e para quaisquer alterações dentro do diretório `docs`. Ele consiste em um único job chamado `deploy` que é executado na versão mais recente do Ubuntu.

### Job: deploy

O job `deploy` é responsável por realizar o deploy da documentação utilizando o MkDocs com o tema Material.

### Steps

1. **Checkout do projeto**: Esta etapa faz o checkout do repositório usando a ação `actions/checkout`.

2. **Configurar credenciais do Git**: Esta etapa configura as credenciais do Git usando o comando `git config` para que o bot do GitHub Actions possa realizar commits.

3. **Configurar Python**: Esta etapa configura a versão do Python usando a ação `actions/setup-python`, onde a versão é definida como `3.x`.

4. **Definir ID do cache**: Esta etapa define uma variável de ambiente `cache_id` que contém o número da semana atual em UTC, utilizando o comando `date`.

5. **Cache para MkDocs Material**: Esta etapa armazena em cache os arquivos usados pelo MkDocs Material usando a ação `actions/cache`. A chave do cache é baseada na variável `cache_id`.

6. **Instalar MkDocs Material**: Esta etapa instala o MkDocs com o tema Material utilizando o `pip`.

7. **Deploy da documentação**: Esta etapa realiza o deploy da documentação para o GitHub Pages usando o comando `mkdocs gh-deploy --force`.

## Pylint

Este fluxo de trabalho do GitHub Actions é acionado em eventos de push para o branch `main` e pull requests. Ele consiste em um único job chamado `lint` que é executado na versão mais recente do Ubuntu.

### Job: lint

O job `lint` usa uma matriz de estratégia para especificar a versão do Python a ser usada. Neste caso, está definido como `3.10`.

### Steps

1. **Checkout do repositório**: Esta etapa faz o checkout do repositório usando a ação `actions/checkout`.

2. **Configurar Python**: Esta etapa configura a versão especificada do Python usando a ação `actions/setup-python`.

3. **Cache pip**: Esta etapa armazena em cache as dependências do pip usando a ação `actions/cache`. A chave de cache é gerada com base no sistema operacional e no hash do arquivo `requirements.txt`.

4. **Instalar dependências**: Esta etapa instala as dependências do projeto executando o comando `pip install`.

5. **Executar Pylint**: Esta etapa executa o Pylint em todos os arquivos `.py` dentro do diretório `forunb/main/`, excluindo os arquivos nas pastas `migrations/`, `management/` e `templatetags/`.


## SonarCloud

Este fluxo de trabalho do GitHub Actions é acionado em eventos de push para os branches `main` e `Development`, bem como em pull requests. Ele consiste em um único job chamado `sonarcloud` que é executado na versão mais recente do Ubuntu.

### Job: sonarcloud

O job `sonarcloud` realiza a análise de código e cobertura de testes utilizando o SonarCloud.

### Steps

1. **Checkout do projeto**: Esta etapa faz o checkout do repositório usando a ação `actions/checkout`.

2. **Configurar Python**: Esta etapa configura a versão especificada do Python usando a ação `actions/setup-python`. A versão do Python é definida pelo uso de uma matriz.

3. **Cache pip**: Esta etapa armazena em cache as dependências do pip usando a ação `actions/cache`. A chave de cache é gerada com base no sistema operacional e no hash do arquivo `requirements.txt`.

4. **Instalar dependências**: Esta etapa instala as dependências do projeto executando o comando `pip install`.

5. **Configurar ambiente**: Esta etapa configura o ambiente de desenvolvimento executando o comando `make config`.

6. **Executar testes com cobertura**: Esta etapa executa os testes do Django utilizando a ferramenta `coverage` para medir a cobertura de código. Em seguida, gera um relatório em formato XML.

7. **Scan do SonarCloud**: Esta etapa executa o scan do SonarCloud, utilizando o token de autenticação armazenado nos segredos do GitHub (`SONAR_TOKEN`) e configurando o caminho para o relatório de cobertura gerado pela etapa anterior.
