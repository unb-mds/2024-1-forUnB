# Use uma imagem base oficial do Python
FROM python:3.11-alpine

# Defina o diretório de trabalho no contêiner
WORKDIR /usr/src/forunb

# definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY ./requirements.txt /usr/src/forunb/requirements.txt

# Atualize o pip para a versão mais recente
RUN pip install --upgrade pip

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação para o contêiner
COPY ./forunb /usr/src/forunb/

# Exponha a porta que o Django usa por padrão
EXPOSE 8000

# Comando para rodar o servidor de desenvolvimento do Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]