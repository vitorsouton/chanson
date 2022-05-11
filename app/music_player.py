import spotipy

from spotipy.oauth2 import SpotifyPKCE
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
                 'user-library-read',
                 'user-top-read'
                 ]
        self.auth = SpotifyPKCE(scope=scope, open_browser=True,
                                 cache_path=cache_path)
        super().__init__(auth_manager=self.auth)
        self.user_id = self.current_user()['id']
        self.playlist_uri = None
        self.playlist_id = None
        self.playlist_name = None
        self.tracks_uri = None
        self.seeds = None
        self.recommendations_uri = None
        self.liked_songs = None


    def get_playlist_info(self):
        playlists = self.current_user_playlists()['items']

        for n in range(len(playlists)):
            if playlists[n]['name'].upper() == 'chanson'.upper():
                self.playlist_uri = playlists[n]['uri']
                self.playlist_id = playlists[n]['id']
                self.playlist_name = playlists[n]['name']

        return self.playlist_uri


    def create_custom_playlist(self):
        self.user_playlist_create(self.user_id, 'Chanson', public=False,
                                  collaborative=False)
        self.get_playlist_info()
        top_tracks = self.current_user_top_tracks(limit=5,
                                                  time_range='short_term')['items']
        top_tracks_uri = [top_tracks[n]['uri'] for n in range(len(top_tracks))]

        self.playlist_add_items(self.playlist_uri, top_tracks_uri)


    def get_tracks_uri(self):
        tracks = self.playlist_tracks(self.playlist_uri)['items']
        self.tracks_uri = [tracks[n]['track']['uri'] for n in range(len(tracks))]


    def clean_playlist(self):
        liked_status = self.current_user_saved_tracks_contains(self.tracks_uri)

        unliked_songs = []
        for track, liked in zip(self.tracks_uri, liked_status):
            if liked is False:
                unliked_songs.append(track)

        self.user_playlist_remove_all_occurrences_of_tracks(
            self.user_id,
            self.playlist_id,
            unliked_songs
        )


    def get_recommendations_uri(self, n_recoms=10):

        self.seeds = sample(self.tracks_uri, 5)

        recommendations = self.recommendations(seed_tracks=self.seeds,
                                               limit=n_recoms)['tracks']
        self.recommendations_uri = [recommendations[n]['uri'] for
                                    n in range(len(recommendations))]


    def add_songs_to_playlist(self):
        self.playlist_add_items(self.playlist_uri, self.recommendations_uri)


if __name__ == '__main__':
    sp = MusicPlayer('vitorrubr')
    info = sp.get_playlist_info()
    if info is None:
        sp.create_custom_playlist()
    sp.get_tracks_uri()
    sp.clean_playlist()
    sp.get_recommendations_uri()
    sp.add_songs_to_playlist()
