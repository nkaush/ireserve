start:
	docker build -t 411-app .
	docker run -it --rm -p 5000:5000 411-app

build:
	docker build -t neilk3/411-flask:latest -f Dockerfile-build .

push: 
	docker push neilk3/411-flask:latest

run:
	docker run -it --rm -p 5000:5000 neilk3/411-flask:latest