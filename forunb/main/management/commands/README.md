# Scraping de Disciplinas do Sigaa da UnB

Este projeto realiza a raspagem das disciplinas disponíveis no site Sigaa da UnB e as salva como fóruns no banco de dados do projeto Django 'ForUnB'.

## Arquivos Principais

- **main/management/commands/scraping_sigaa.py**
- **main/scraping.py**

## Descrição dos Arquivos

### scraping_sigaa.py

Este é um comando personalizado do Django que executa a raspagem das disciplinas do Sigaa da UnB e cria fóruns correspondentes no banco de dados.

#### Funcionalidades:
- Deleta todos os fóruns existentes para evitar duplicações.
- Raspa as disciplinas de departamentos específicos para um determinado ano e período.
- Cria novos fóruns no banco de dados para cada disciplina raspada.

### scraping.py
Este arquivo contém a lógica de raspagem propriamente dita. Ele define a classe `DisciplineWebScraper`, que lida com as requisições HTTP ao site Sigaa e a extração dos dados das disciplinas.

#### Funcionalidades:
- Faz uma requisição POST ao Sigaa com os dados do departamento, ano e período.
- Analisa a resposta do Sigaa e extrai as disciplinas em uma tabela.
- Organiza as disciplinas em um dicionário que é retornado para ser utilizado no comando Django.

## Como Usar

Execute o comando de raspagem:
```bash
python manage.py scraping_sigaa
```