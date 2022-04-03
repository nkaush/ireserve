PORT=8080

start:
	docker build -t 411-app .
	docker run -it --rm -p $(PORT):$(PORT) 411-app

<<<<<<< HEAD
local:
	docker build -t 411-app -f Dockerfile-build .; docker run -it --rm -p 8080:8080 411-app
=======
develop:
	docker build -t 411-develop -f Dockerfile-develop .
	docker run -it --rm -p 8080:8080 -v `pwd`/flask-app:/flaskr 411-develop
>>>>>>> 63ce7b11819edcf8919e4036f609393f506117d1

build:
	docker build -t neilk3/411-flask:latest -f Dockerfile-build .

run:
	docker run -it --rm -p $(PORT):$(PORT) neilk3/411-flask:latest

push: 
	docker push neilk3/411-flask:latest

waitress:
	waitress-serve --port=$(PORT) --call app:create_app

# gcloud auth login
# gcloud config set project cs-411-final-project-342117
gcp-deploy:
	gcloud builds submit --tag gcr.io/cs-411-final-project-342117/ireserve
	gcloud run deploy --image gcr.io/cs-411-final-project-342117/ireserve --platform managed