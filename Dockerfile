FROM python:3.10.4-buster

COPY . /app

RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "vim"]

WORKDIR /app

RUN pip install -r requirements.txt

COPY chanson/auth_backup/oauth2.py ./usr/local/lib/python3.10/site-packages/spotipy

EXPOSE 3002
EXPOSE 1337

ENTRYPOINT [ "python" ]

CMD [ "chanson/app.py" ]
