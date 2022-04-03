build:
	docker build -t neilk3/411-flask:latest .

push: 
	docker push neilk3/411-flask:latest

run:
	docker run -it --rm -p 5000:5000 neilk3/411-flask:latest