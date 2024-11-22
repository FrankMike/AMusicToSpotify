from apple_music import AppleMusicClient
from spotify import SpotifyClient
import os


def transfer_playlist(playlist_name, new_playlist_name):
    # Initialize clients
    apple_music = AppleMusicClient()

    # Check if library file exists
    if not os.path.exists(apple_music.library_path):
        print(f"iTunes Library file not found at: {apple_music.library_path}")
        alt_path = os.path.expanduser("~/Music/Music/Library.xml")
        if os.path.exists(alt_path):
            print(f"Found Library file at alternate location: {alt_path}")
            apple_music.library_path = alt_path
        else:
            print("\nCouldn't find iTunes Library XML file.")
            print("Please make sure to enable XML sharing in iTunes/Music preferences:")
            print(
                "iTunes/Music -> Preferences -> Advanced -> Share iTunes Library XML with other applications"
            )
            return

    # Get tracks from iTunes Library
    print("Fetching tracks from iTunes Library...")
    tracks = apple_music.get_playlist(playlist_name)

    if not tracks:
        print(f"Failed to fetch tracks from playlist: {playlist_name}")
        return

    if len(tracks) == 0:
        print(f"No tracks found in playlist: {playlist_name}")
        return

    print(f"Found {len(tracks)} tracks")

    # Initialize Spotify client and create playlist
    try:
        spotify = SpotifyClient()
        print("Creating Spotify playlist...")
        playlist_id = spotify.create_playlist(new_playlist_name, tracks)

        if playlist_id:
            print(f"Successfully created Spotify playlist! ID: {playlist_id}")
        else:
            print("Failed to create Spotify playlist")
    except Exception as e:
        print(f"Error with Spotify: {str(e)}")


if __name__ == "__main__":
    print("iTunes/Music to Spotify Playlist Transfer")
    print("----------------------------------------")
    playlist_name = input("Enter iTunes/Music playlist name: ")
    new_playlist_name = input("Enter new Spotify playlist name: ")
    transfer_playlist(playlist_name, new_playlist_name)
