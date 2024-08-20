## Descrição
Este script Python é utilizado para gerar um arquivo .env para um projeto Django. O arquivo .env é essencial em projetos Django, pois armazena **variáveis de ambiente**, como a chave secreta (`SECRET_KEY`), que são necessárias para a execução segura do projeto.
Este arquivo deve ser executado antes de rodar o ambiente localmente com o uso do Makefile.
```bash
make config
```

## Como o Script Funciona
É feito uma leitura no arquivo `.env.example` onde  estão armazenados as variáveis de ambiente padrão do projeto. O script lê o conteúdo do arquivo `.env.example` e cria um novo arquivo `.env` com o mesmo ambiente de produção (local) e inicializa a chave secreta (SECRET_KEY) com um valor aleatório, que é geredo por uma biblioteca do Django.

## Uso
Execute o script em um ambiente Python onde o Django esteja instalado. Certifique-se de que o caminho para o arquivo .env.example esteja correto, conforme definido no script.

```bash
python config.py
```


Exemplo de Saída
```bash
.env file created successfully at /2024-1forunb/forunb/.env
```