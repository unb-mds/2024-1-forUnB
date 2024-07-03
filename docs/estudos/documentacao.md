# MkDocs

## O que é?

É uma biblioteca do python que utiliza da lingaugem de [Markdown](https://en.wikipedia.org/wiki/Markdown) para gerar uma documentação para um projeto. No qual há um único arquivo YAML para ser configurado.

## Como usar?

### 1. Preparando o ambiente

Para começar a usar é importante ter o python baixdo na sua máquina na versão mais recente, além do gerenciador de pacotes do python, pip, para isso basta:

```bash
$ python --version

$ pip --version
```

Caso não tenha em sua máquina confira o link:

- [Como baixar o python com o pip](https://docs.python.org/3/using/unix.html)

### 2. Baixando o MkDocs

Com o ambiente pronto, agora basta apenas utilizar o pip para baixar o MkDocs

```bash
$ pip install mkdocs
```

### 3. Criando um novo projeto

Para começar a utilizar o MkDocs é necessário rodar este comando

```bash
$ mkdocs new my-project

$ cd my-project
```

Com esse comando o MkDocs criará uma pasta chamada "my-project", nela terá a pasta principal da documentação `docs` e o seu arquivo YMAL, `mkdocs.yml`

### 4. Visualizando o projeto

Com a criação destes arquivos o MkDocs vem com uma função built-in que prepara um servidor local. Para isso basta estar no mesmo diretório do arquvio `mkdocs.yml`

```bash
$ mkdocs serve
```

### 5. Criando a build

Por fim, para criar a primeira build do projeto basta executar o código:

```bash
$ mkdocs build
```

## Github

Para conseguir utilizar esta documentação no próprio GitHub é necessário algumas etapas:

1.  Todo o código já deve ter uma build.
2. Utilizar o comando `mkdocs gh-deploy` para criar um nova branch chamda `gh-pages`.
3. Utilizar o [GitHub Pages](https://pages.github.com/) para hospedar o código que ficou na nova branch.

**obs:** Não se pode alterar nenhum arquivo direto na branch gerada `gh-pages`. Deve-se usar o intermédio do `mkdocs gh-deploy`.