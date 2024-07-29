install:
	python3 -m pip install --upgrade pip 
	python3 -m pip install -r requirements.txt

build:
	docker build -t forunb .

run:
	docker run -p 8000:8000 forunb