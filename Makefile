PORT=8080

start:
	docker build -t 411-app .
	docker run -it --rm -p $(PORT):$(PORT) 411-app

local:
	docker build -t neilk3/411-flask:latest -f Dockerfile-build .
	docker run -it --rm -p $(PORT):$(PORT) neilk3/411-flask:latest

build:
	docker build -t neilk3/411-flask:latest -f Dockerfile-build .

push: 
	docker push neilk3/411-flask:latest

run:
	docker run -it --rm -p $(PORT):$(PORT) neilk3/411-flask:latest

waitress:
	waitress-serve --port=$(PORT) --call app:create_app

# gcloud auth login
# gcloud config set project cs-411-final-project-342117
gcp-deploy:
	gcloud builds submit --tag gcr.io/cs-411-final-project-342117/ireserve
	gcloud run deploy --image gcr.io/cs-411-final-project-342117/ireserve --platform managed