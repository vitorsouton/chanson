FROM python:3.10.4-buster

COPY . /app

RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "vim"]
RUN pip install -r app/requirements.txt

COPY chanson/auth_backup/oauth2.py /usr/local/lib/python3.10/site-packages/spotipy/oauth2.py

EXPOSE 3002
EXPOSE 1337

WORKDIR /app

ENTRYPOINT [ "python" ]

CMD [ "chanson/app.py" ]
