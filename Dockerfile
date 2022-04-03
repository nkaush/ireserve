FROM python:3.9.12-buster

COPY /flask-app/ /flaskr

WORKDIR /flaskr

EXPOSE 5000

RUN pip install -r requirements.txt

ENTRYPOINT [ "/bin/sh" ]

# ENTRYPOINT ["/usr/local/bin/python -m flask run --host=0.0.0.0"]

# CMD ["python -m flask run --host=0.0.0.0"]

# ENTRYPOINT [ "python" ]
# CMD [ "app.py" ]