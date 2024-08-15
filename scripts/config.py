import os
from django.core.management.utils import get_random_secret_key

# Definindo os paths dos arquivos .env.example e .env
env_example_path = './forunb/.env.example'
env_path = './forunb/.env'

# Lendo o arquivo .env.example
with open(env_example_path, 'r') as example_file:
    lines = example_file.readlines()

# Separando as linhas do arquivo .env.example
new_env_lines = []
for line in lines:
    if line.startswith('SECRET_KEY'):
        # Gerando uma nova chave secreta
        secret_key = get_random_secret_key()
        new_env_lines.append(f"SECRET_KEY='{secret_key}'\n")
    else:
        new_env_lines.append(line)

# Escrevendo no arquivo .env
with open(env_path, 'w') as env_file:
    env_file.writelines(new_env_lines)

print(f".env file created successfully at {os.path.abspath(env_path)}")
