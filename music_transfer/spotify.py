import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI


class SpotifyClient:
    def __init__(self):
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET,
                redirect_uri=SPOTIFY_REDIRECT_URI,
                scope="playlist-modify-public",
            )
        )

    def create_playlist(self, name, tracks):
        """
        Create a new playlist and add tracks to it
        """
        try:
            # Create new playlist
            user_id = self.sp.current_user()["id"]
            playlist = self.sp.user_playlist_create(user_id, name)

            # Search and add tracks
            track_uris = []
            for track in tracks:
                query = f"track:{track['name']} artist:{track['artist']}"
                result = self.sp.search(query, type="track", limit=1)

                if result["tracks"]["items"]:
                    track_uris.append(result["tracks"]["items"][0]["uri"])

            # Add tracks in batches of 100 (Spotify API limit)
            for i in range(0, len(track_uris), 100):
                batch = track_uris[i : i + 100]
                self.sp.playlist_add_items(playlist["id"], batch)

            return playlist["id"]
        except Exception as e:
            print(f"Error creating playlist: {e}")
            return None
