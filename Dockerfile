FROM python:3.10.4-buster

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "chanson/app.py" ]
