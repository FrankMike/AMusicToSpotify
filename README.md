# Apple Music to Spotify Playlist Transfer

A Python tool to transfer your playlists from Apple Music to Spotify. This tool allows you to transfer either individual playlists or all playlists at once.

## Features

- Transfer a single playlist from Apple Music to Spotify
- Transfer all playlists from Apple Music to Spotify
- Automatic matching of songs between platforms
- Support for large playlists (handles Spotify's API limits)

## Prerequisites

- Python 3.6 or higher
- Apple Music with XML Library sharing enabled
- Spotify account
- Spotify Developer credentials

## Installation

1. Clone the repository:

```bash
git clone https://github.com/FrankMike/AMusicToSpotify.git
cd AMusicToSpotify
```

2. Install required dependencies:

```bash
# Generate and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

cd music_transfer

# Install dependencies from the requirements.txt file
pip install -r requirements.txt
```


3. Enable XML sharing in Apple Music:
   - Open Apple Music
   - Go to File > Library > Export Library

4. Set up Spotify Developer credentials:
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Create a new application
   - Get your Client ID and Client Secret
   - Add `http://localhost:8888/callback` to your Redirect URIs in the app settings

5. Create a `.env` file in the project root with your Spotify credentials:

```bash
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
```

## Usage

Run the main script:

```bash
python music_transfer/main.py
```

Follow the prompts to choose between:
1. Transferring a single playlist
2. Transferring all playlists

### Single Playlist Transfer
- Enter the exact name of your Apple Music playlist
- Enter the desired name for the new Spotify playlist

### All Playlists Transfer
- The script will automatically transfer all non-empty playlists from Apple Music to Spotify
- Playlists will keep their original names

## Troubleshooting

- If the Apple Music Library XML file is not found in the default location, the script will check the alternate location and prompt you to enable XML sharing if needed.
- If songs aren't matching correctly, check that the song titles and artist names are similar between platforms.
- Make sure your Spotify credentials are correct and you have the necessary permissions.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.