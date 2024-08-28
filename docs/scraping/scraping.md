# Raspagem de Disciplinas do Sigaa da UnB
O scraping realizado têm a finalidade de realizar a raspagem de dados das disciplinas disponíveis no site Sigaa da UnB e salvar essas disciplinas como fóruns no banco de dados do projeto Django 'ForUnB', possuindo dois arquivos principais.

## Arquivos Principais

- **main/management/commands/scraping_sigaa.py**
- **main/scraping.py**

## Descrição dos Arquivos

### **1. scraping_sigaa.py**
Esse arquivo é um comando customizado do Django que realiza a raspagem das disciplinas do site Sigaa da UnB e as salva como fóruns no banco de dados do projeto. Ele faz uso de um raspador de dados implementado na classe DisciplineWebScraper, que está definida no arquivo main/scraping.py.

#### Funcionamento:
- **Comando Personalizado:** A classe Command herda de BaseCommand, que permite a criação de comandos personalizados que podem ser executados via terminal usando python manage.py scraping_sigaa.
- **Parâmetros de Configuração:** São definidos parâmetros como os departamentos (departments), o ano (year) e o período (period) para especificar quais disciplinas serão raspadas.
- **Deleção de Fóruns Antigos:** Antes de iniciar a raspagem, o código deleta todos os fóruns existentes no banco de dados para evitar duplicações.
- **Raspagem e Criação de Fóruns:** Para cada departamento especificado, o código utiliza o DisciplineWebScraper para obter as disciplinas. Em seguida, cria um fórum no banco de dados para cada disciplina encontrada. Se um fórum já existir, o código apenas avisa que ele já estava presente.

### **2. scraping.py**
Esse arquivo contém a lógica para a raspagem das disciplinas a partir do site Sigaa da UnB. Ele define a classe DisciplineWebScraper e algumas funções auxiliares para realizar essa tarefa.

#### Funcionamento:
- **Sessão e Cookies:** O raspador inicia criando uma sessão de requisição HTTP e obtendo os cookies necessários para realizar as requisições no site Sigaa.
- **Raspagem das Disciplinas:**

    -- ***'get_response_from_disciplines_post_request':*** Essa função faz uma requisição POST ao site Sigaa com os dados do departamento, ano e período para obter a lista de disciplinas.

    -- ***'make_web_scraping_of_disciplines':*** Após receber a resposta, essa função analisa o conteúdo HTML da página para encontrar a tabela que contém as disciplinas. Ela extrai as informações de cada disciplina e as organiza em um dicionário onde as chaves são os códigos das disciplinas e os valores são listas com os nomes das disciplinas correspondentes.

- **Retorno dos Dados:** O método get_disciplines retorna o dicionário contendo os códigos das disciplinas como chaves e os nomes das disciplinas como valores.

## Como Usar

 Execute o comando de raspagem:

   ```
   $ python manage.py scraping_sigaa
   ```