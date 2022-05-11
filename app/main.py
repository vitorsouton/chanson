import os

from flask import Flask, render_template, request
from app.music_player import MusicPlayer

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def get_info():
    username = request.form.get('campoUsername')
    sp = MusicPlayer(username)

    info = sp.get_playlist_info()
    if info is None:
        sp.create_custom_playlist()
    sp.get_tracks_uri()
    sp.clean_playlist()
    sp.get_recommendations_uri()
    sp.add_songs_to_playlist()

    playlist = sp.playlist_name

    return render_template('playlists.html',
                           playlist=playlist)
