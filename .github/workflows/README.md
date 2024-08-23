# Descrição do funcionamento dos workflows
Os workflows são arquivos de configuração que definem um conjunto de ações que devem ser executadas em resposta a eventos específicos. Eles são compostos por jobs, que são executados em paralelo, e por steps, que são executados sequencialmente. Cada step é composto por uma ou mais ações, que são executadas em um ambiente específico. Dessa forma, separamos em 4 workflows:
    
- **CI**: responsável por executar os testes automatizados e garantir a qualidade do código.
- **docs**: responsável por gerar a documentação do projeto.
- **pylint**: responsável por executar o linting do código.
- **sonar**: responsável por enviar as métricas de qualidade do código para o SonarCloud.

## CI

Este fluxo de trabalho do GitHub Actions é acionado em eventos de push para o branch `main` e em pull requests. Ele executa testes unitários em uma matriz de versões do Python.

### Job: u-tests

O job `u-tests` é responsável por configurar o ambiente necessário e executar os testes unitários do projeto.

### Steps

1. **Checkout do projeto**: Esta etapa faz o checkout do repositório usando a ação `actions/checkout`.

2. **Configurar Python ${{ matrix.python-version }}**: Esta etapa configura a versão do Python definida na matriz, utilizando a ação `actions/setup-python`.

3. **Cache do pip**: Esta etapa armazena em cache os pacotes instalados pelo pip, para acelerar as execuções subsequentes. A chave do cache é gerada a partir do sistema operacional do runner e do hash do arquivo `requirements.txt`.

4. **Instalar dependências**: Nesta etapa, o pip é atualizado e as dependências do projeto são instaladas a partir do arquivo `requirements.txt`.

5. **Instalar PostgreSQL**: Esta etapa instala o PostgreSQL no ambiente de execução.

6. **Iniciar PostgreSQL**: Esta etapa inicia o serviço do PostgreSQL.

7. **Configurar PostgreSQL**: Nesta etapa, o banco de dados e o usuário necessários para os testes são criados e configurados no PostgreSQL.

8. **Configurar ambiente**: Esta etapa executa o comando `make config` para configurar o ambiente necessário para os testes.

9. **Executar testes**: Finalmente, esta etapa executa os testes unitários do projeto usando o comando `python ./forunb/manage.py test forunb`.

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

Este fluxo de trabalho do GitHub Actions é acionado em eventos de push para o branch `main` e em pull requests. Ele executa a verificação de linting do código Python utilizando o Pylint.

### Job: lint

O job `lint` é responsável por verificar a qualidade do código Python utilizando o Pylint.

### Steps

1. **Checkout do repositório**: Esta etapa faz o checkout do repositório usando a ação `actions/checkout`.

2. **Configurar Python ${{ matrix.python-version }}**: Esta etapa configura a versão do Python definida na matriz, utilizando a ação `actions/setup-python`.

3. **Cache do pip**: Esta etapa armazena em cache os pacotes instalados pelo pip para acelerar as execuções subsequentes. A chave do cache é gerada a partir do sistema operacional do runner e do hash do arquivo `requirements.txt`.

4. **Instalar dependências**: Nesta etapa, o pip é atualizado e as dependências do projeto são instaladas a partir do arquivo `requirements.txt`.

5. **Executar Pylint**: Nesta etapa, o Pylint é executado em todos os arquivos Python dentro do diretório `forunb`, exceto nos diretórios `migrations` e `management`, além dos diretórios `templatetags`. O resultado da execução é salvo em um arquivo `pylint_output.txt`.

    - **Analisar resultado do Pylint**: O score final do Pylint é extraído do relatório e exibido. Se o score for maior que 8, o job é considerado bem-sucedido. Caso contrário, o job falha, e uma mensagem informando o score é exibida.

## SonarCloud

Este fluxo de trabalho do GitHub Actions é acionado em eventos de push para os branches `main` e `Development`, bem como em pull requests. Ele executa uma análise de código utilizando o SonarCloud, além de configurar o ambiente de teste e executar os testes com cobertura de código.

### Job: sonarcloud

O job `sonarcloud` é responsável por configurar o ambiente, executar os testes com cobertura e realizar a análise de código com o SonarCloud.

### Steps

1. **Checkout do projeto**: Esta etapa faz o checkout do repositório usando a ação `actions/checkout`.

2. **Configurar Python ${{ matrix.python-version }}**: Esta etapa configura a versão do Python utilizando a ação `actions/setup-python`.

3. **Cache do pip**: Esta etapa armazena em cache os pacotes instalados pelo pip para acelerar as execuções subsequentes. A chave do cache é gerada a partir do sistema operacional do runner e do hash do arquivo `requirements.txt`.

4. **Instalar dependências**: Nesta etapa, o pip é atualizado e as dependências do projeto são instaladas a partir do arquivo `requirements.txt`.

5. **Instalar PostgreSQL**: Esta etapa instala o PostgreSQL no ambiente de execução.

6. **Iniciar PostgreSQL**: Esta etapa inicia o serviço do PostgreSQL.

7. **Configurar PostgreSQL**: Nesta etapa, o banco de dados e o usuário necessários para os testes são criados e configurados no PostgreSQL.

8. **Configurar ambiente**: Esta etapa executa o comando `make config` para configurar o ambiente necessário para os testes.

9. **Executar testes com cobertura**: Nesta etapa, os testes do projeto são executados utilizando o `coverage`, e um relatório XML da cobertura de código é gerado.

10. **SonarCloud Scan**: Finalmente, o SonarCloud é utilizado para realizar a análise de código. As variáveis de ambiente `GITHUB_TOKEN` e `SONAR_TOKEN` são usadas para autenticação e configuração. O relatório de cobertura de código gerado na etapa anterior é passado para o SonarCloud através do argumento `-Dsonar.python.coverage.reportPaths=coverage.xml`.

