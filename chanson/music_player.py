import re
import spotipy

from spotipy.oauth2 import SpotifyOAuth
from dotenv import find_dotenv, load_dotenv
from random import sample


class MusicPlayer(spotipy.Spotify):

    def __init__(self, username):
        env_path = find_dotenv()
        load_dotenv(env_path)


        cache_path = f'./chanson/users/.cache-{username}'

        scope = ["playlist-read-private",
                 "playlist-read-collaborative",
                 "playlist-modify-public",
                 "playlist-modify-private",
                 'user-library-read'
                 ]
        self.auth = SpotifyOAuth(scope=scope, open_browser=True,
                                 cache_path=cache_path)
        super().__init__(auth_manager=self.auth)
        self.user_id = self.current_user()['id']
        self.playlist_uri = None
        self.tracks_uri = None
        self.seeds = None
        self.recommendations_uri = None
        self.liked_songs = None


    def get_playlist_uri(self):
        playlists = self.current_user_playlists()['items']

        for n in range(len(playlists)):
            if playlists[n]['name'].upper() == 'novas musicas'.upper():
                self.playlist_uri = playlists[n]['uri']


    def get_recommendations_uri(self, n_recoms=10):
        tracks = self.playlist_tracks(self.playlist_uri)['items']
        self.tracks_uri = [tracks[n]['track']['uri'] for n in range(len(tracks))]
        self.seeds = sample(self.tracks_uri, 5)

        recommendations = self.recommendations(seed_tracks=self.seeds,
                                               limit=n_recoms)['tracks']
        self.recommendations_uri = [recommendations[n]['uri'] for
                                    n in range(len(recommendations))]


    def add_songs_to_playlist(self):
        self.playlist_add_items(self.playlist_uri, self.recommendations_uri)


if __name__ == '__main__':
    sp = MusicPlayer('vitorrubr')
    sp.get_playlist_uri()
    sp.get_recommendations_uri()
    sp.add_songs_to_playlist()
    print(sp.recommendations_uri)
