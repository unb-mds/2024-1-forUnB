# [ForUnB](https://unb-mds.github.io/2024-1-forUnB/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=unb-mds_2024-1-forUnB&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=unb-mds_2024-1-forUnB)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=unb-mds_2024-1-forUnB&metric=coverage)](https://sonarcloud.io/summary/new_code?id=unb-mds_2024-1-forUnB)
[![GitHub issues](https://img.shields.io/github/issues/unb-mds/2024-1-forunb)](https://github.com/unb-mds/2024-1-forUnB/issues)
[![GitHub contributors](https://img.shields.io/github/contributors/unb-mds/2024-1-forunb)](https://github.com/unb-mds/2024-1-forUnB/graphs/contributors)

[![Python version](https://img.shields.io/badge/python-3.10.12-blue)](https://www.python.org/)
[![Django version](https://img.shields.io/badge/django-4.2.14-blue)](https://www.djangoproject.com/)

O ForUnB é um projeto da disciplina **Métodos de Desenvolvimento de Software**, que tem como objetivo incentivar os alunos da Universidade de Brasília, campus Gama (UnB), a tirar dúvidas sobre qualquer matéria por meio de um fórum.

O projeto é software livre e está sob a licença [MIT](./LICENSE).

## 📝 Sumário

- [📝 Sumário](#-sumário)
- [👥 Equipe de Desenvolvimento](#-equipe-de-desenvolvimento)
- [✨ Início](#-início)
    - [📋 Pré-requisitos](#-pré-requisitos)
    - [💻 Ambiente](#-ambiente)
    - [📁 Dependências do projeto](#-dependências-do-projeto)
    - [💾 Execução](#-execução)
- [📚 Documentação](#-documentação)
- [🛠️ Protótipos](#protótipos)
- [✨ User Story Mapping](#-user-story-mapping)
- [👥 Equipe de Desenvolvimento](#-equipe-de-desenvolvimento)


## ✨ Início

Você pode clonar o repositório do projeto com o seguinte comando:

```bash
git clone https://github.com/unb-mds/2024-1-forUnB.git
```

### 📋 Pré-requisitos

Para rodar o projeto, você precisa instalar as dependências globais, que são:

- [GNU Make](https://www.gnu.org/software/make/#download) 4.3 (ou superior);
- [Python](https://www.python.org/downloads/release/python-31012/) v3.10.12;
- [Pip](https://packaging.python.org/en/latest/tutorials/installing-packages/) v24.2 (ou superior);
- [Venv](https://docs.python.org/3/library/venv.html), módulo  do Python.

### 💻 Ambiente

Para configurar o ambiente basta seguir este script. 

```bash
make config
```
> **Observação:** Este comando criará uma pasta .env com as variáveis de ambiente necessárias para o projeto.
### 📁 Dependências do projeto

```bash
# Cria um ambiente virtual Python e instala as dependências do projeto:
python3 -m venv .venv

# Com o ambiente virtual criado, ative-o:
source .venv/bin/activate

# Faça a instalação das dependências do projeto:
make install
```

### No Windows:

Para ativiar o ambiente basta 

```bash
.venv\Scripts\activate
```

Quando o ambiente virtual estiver ativado, você verá (venv) antes do prompt de comando, indicando que o ambiente virtual está em uso.

### 💾 Execução

Para executar o projeto em **ambiente local**, você pode rodar entrar na pasta onde se encontra o arquivo manage.py e rodar os seguintes comandos:

```bash
# Crie as migrações
python3 manage.py makemigrations

# Aplique as migrações
python3 manage.py migrate

# Rode o servidor local
python3 manage.py runserver
```

## 📚 Documentação
        
Documentação do projeto pode ser acessada [aqui](https://unb-mds.github.io/2024-1-forUnB/).

## 🛠️ Protótipos 

### Protótipo de baixa fidelidade
- Para acesar clique [aqui](https://www.figma.com/proto/ktEvIqEpgsThoDwnXSdD3Y/Prototipo-de-baixa-fidelidade?node-id=2-2&mode=design&t=eiqpzf5QcevaT4Ok-1).

### Protótipo de alta fidelidade
- Para acesar clique [aqui](https://www.figma.com/proto/kI9C8oLfBGGoXdJU1zAdZX/Intera%C3%A7%C3%B5es?node-id=1-2&starting-point-node-id=1%3A2&mode=design&t=tLNIpJGRjTw0PVRe-1).

## ✨ User Story Mapping

### Miro
- Para acessar clique [aqui](https://miro.com/app/board/uXjVK3aRJY0=/?share_link_id=690300696919).


## 👥 Equipe de Desenvolvimento

<center>
    <table style="margin-left: auto; margin-right: auto;">
        <tr>
            <td align="center">
                <a href="https://github.com/AlexandreLJr">
                    <img style="border-radius: 50%;" src="https://github.com/AlexandreLJr.png" width="150px;"/>
                    <h5 class="text-center">Alexandre<br>Junior</h5>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/BrunoBReis">
                    <img style="border-radius: 50%;" src="https://github.com/BrunoBReis.png" width="150px;"/>
                    <h5 class="text-center">Bruno<br>Bragança</h5>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/davi-Klevy">
                    <img style="border-radius: 50%;" src="https://github.com/davi-Klevy.png" width="150px;"/>
                    <h5 class="text-center">Davi<br>Klein</h5>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/manu-sgc">
                    <img style="border-radius: 50%;" src="https://github.com/manu-sgc.png" width="150px;"/>
                    <h5 class="text-center">Manoela<br>Garcia</h5>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/pLopess">
                    <img style="border-radius: 50%;" src="https://github.com/pLopess.png" width="150px;"/>
                    <h5 class="text-center">Pedro<br>Lopes</h5>
                </a>
            </td>
        <td align="center">
                <a href="https://github.com/VHbernardes">
                    <img style="border-radius: 50%;" src="https://github.com/VHbernardes.png" width="150px;"/>
                    <h5 class="text-center">Victor Hugo<br>Bernardes</h5>
                </a>
            </td>
    </table>

</center>
