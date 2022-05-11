import spotipy

from spotipy.oauth2 import SpotifyOAuth
from dotenv import find_dotenv, load_dotenv


class MusicPlayer(spotipy.Spotify):

    def __init__(self):
        env_path = find_dotenv()
        load_dotenv(env_path)

        cache_path = 'users/.cache'

        scope = ["playlist-read-private",
                 "playlist-modify-public",
                 "playlist-modify-private"
                 ]
        self.auth = SpotifyOAuth(scope=scope, open_browser=True,
                                 cache_path=cache_path)
        super().__init__(auth_manager=self.auth)
        self.user_id = self.current_user()['id']


if __name__ == '__main__':
    sp = MusicPlayer()
    print(sp.user_id)
