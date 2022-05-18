import os
import uuid
import spotipy

from dotenv import find_dotenv, load_dotenv
from flask import Flask, request, redirect, session, render_template
from flask_session import Session
from app.music_player import MusicPlayer
from app.auth_backup.oauth2 import SpotifyOAuth

env_path = find_dotenv()
load_dotenv(env_path)

app = Flask(__name__)
app.config['SECRECT_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

caches_folder = './app/users/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

def session_cache_path():
    return caches_folder + session.get('uuid')


@app.route('/', methods=['GET', 'POST'])
def index():
    global sp

    scope = ["playlist-read-private",
                 "playlist-read-collaborative",
                 "playlist-modify-public",
                 "playlist-modify-private",
                 'user-library-read',
                 'user-top-read'
                 ]

    if not session.get('uuid'):
        session['uuid'] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    auth_manager = SpotifyOAuth(scope=scope, cache_handler=cache_handler, show_dialog=True)

    if request.args.get('code'):
        auth_manager.get_access_token(request.args.get('code'))
        return redirect('/')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        auth_url = auth_manager.get_authorize_url()
        return f'<h2><a href="{auth_url}">Sign in</a></h2>'


    if request.method == 'POST':
        run = request.form.get('run')
        if run == 'run':
            sp = MusicPlayer(auth=auth_manager)
            print(sp.user_id)
            return redirect('/done')


    return render_template('index.html')


@app.route('/done')
def done():
    info = sp.get_playlist_info()
    if info is None:
        sp.create_custom_playlist()
    sp.get_tracks_uri()
    sp.clean_playlist()
    sp.remove_liked_duplicates()
    sp.get_recommendations_uri()
    sp.add_songs_to_playlist()

    user_id = sp.user_id

    return render_template('playlists.html',
                           user_id=user_id)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
