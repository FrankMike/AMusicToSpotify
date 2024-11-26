from apple_music import AppleMusicClient
from spotify import SpotifyClient
import os


def transfer_single_playlist(apple_music, spotify, playlist_name, new_playlist_name):
    """Transfer a single playlist from Apple Music to Spotify"""
    print(f"Fetching tracks from Apple Music playlist: {playlist_name}")
    tracks = apple_music.get_playlist(playlist_name)

    if not tracks:
        print(f"Failed to fetch tracks from playlist: {playlist_name}")
        return False

    if len(tracks) == 0:
        print(f"No tracks found in playlist: {playlist_name}")
        return False

    print(f"Found {len(tracks)} tracks")

    print("Creating Spotify playlist...")
    playlist_id = spotify.create_playlist(new_playlist_name, tracks)

    if playlist_id:
        print(f"Successfully created Spotify playlist! ID: {playlist_id}")
        return True
    else:
        print("Failed to create Spotify playlist")
        return False


def transfer_all_playlists(apple_music, spotify):
    """Transfer all playlists from Apple Music to Spotify"""
    print("Fetching all playlists from Apple Music...")
    playlists = apple_music.get_all_playlists()

    if not playlists:
        print("Failed to fetch playlists from Apple Music")
        return

    print(f"Found {len(playlists)} playlists")
    successful = 0

    for playlist_name, tracks in playlists.items():
        print(f"\nProcessing playlist: {playlist_name}")
        if len(tracks) == 0:
            print("Skipping empty playlist")
            continue

        print(f"Found {len(tracks)} tracks")
        print("Creating Spotify playlist...")

        playlist_id = spotify.create_playlist(f"{playlist_name}", tracks)
        if playlist_id:
            print(f"Successfully created Spotify playlist! ID: {playlist_id}")
            successful += 1
        else:
            print("Failed to create Spotify playlist")

    print(
        f"\nTransfer complete! Successfully transferred {successful} out of {len(playlists)} playlists"
    )


def main():
    print("Apple Music to Spotify Playlist Transfer")
    print("----------------------------------------")

    # Initialize clients
    apple_music = AppleMusicClient()

    # Check if library file exists
    if not os.path.exists(apple_music.library_path):
        print(f"Apple Music Library file not found at: {apple_music.library_path}")
        alt_path = os.path.expanduser("~/Music/Music/Library.xml")
        if os.path.exists(alt_path):
            print(f"Found Library file at alternate location: {alt_path}")
            apple_music.library_path = alt_path
        else:
            print("\nCouldn't find Apple Music Library XML file.")
            print("Please make sure to enable XML sharing in Apple Music preferences:")
            print(
                "Apple Music -> Preferences -> Advanced -> Share Apple Music Library XML with other applications"
            )
            return

    # Initialize Spotify client
    try:
        spotify = SpotifyClient()
    except Exception as e:
        print(f"Error with Spotify: {str(e)}")
        return

    # Ask user for transfer mode
    print("\nChoose transfer mode:")
    print("1. Transfer single playlist")
    print("2. Transfer all playlists")

    while True:
        choice = input("Enter your choice (1 or 2): ").strip()
        if choice in ["1", "2"]:
            break
        print("Invalid choice. Please enter 1 or 2.")

    if choice == "1":
        playlist_name = input("Enter Apple Music playlist name: ")
        new_playlist_name = input("Enter new Spotify playlist name: ")
        transfer_single_playlist(apple_music, spotify, playlist_name, new_playlist_name)
    else:
        transfer_all_playlists(apple_music, spotify)


if __name__ == "__main__":
    main()
