## Make file ##

# Configuration
config: 
	python3 ./scripts/config.py

# Install Django dependencies
install:
	python3 -m pip install --upgrade pip 
	python3 -m pip install -r forunb/requirements.txt

# Migratons
makemigration:
	python3 manage.py makemigrations
migrate:
	python3 manage.py migrate

## Docker ##
build:
	docker build -t forunb .

run:
	docker run -p 8000:8000 forunb