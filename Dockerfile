FROM python:3.8

RUN pip install flask

WORKDIR /app

ADD * /app/

CMD [ "python", "main.py" ]