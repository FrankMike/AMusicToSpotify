import xml.etree.ElementTree as ET
import os


class AppleMusicClient:
    def __init__(self):
        # Default Apple Music Library XML location on macOS
        self.library_path = os.path.expanduser("~/Music/Music/Library.xml")

    def get_playlist(self, playlist_name):
        """
        Fetch a playlist and its tracks from Apple Music Library XML
        """
        try:
            tree = ET.parse(self.library_path)
            root = tree.getroot()

            tracks = {}
            playlists = []

            # First, get all tracks
            for dict_elem in root.findall(".//dict"):
                keys = [k.text for k in dict_elem.findall("key")]
                if "Tracks" in keys:
                    tracks_dict = dict_elem.find("dict")
                    for track in tracks_dict.findall("dict"):
                        track_keys = [k.text for k in track.findall("key")]
                        track_values = track.findall("*")[1::2]  # Get all values

                        if "Track ID" in track_keys:
                            idx = track_keys.index("Track ID")
                            track_id = track_values[idx].text

                            name_idx = (
                                track_keys.index("Name") if "Name" in track_keys else -1
                            )
                            artist_idx = (
                                track_keys.index("Artist")
                                if "Artist" in track_keys
                                else -1
                            )
                            album_idx = (
                                track_keys.index("Album")
                                if "Album" in track_keys
                                else -1
                            )

                            tracks[track_id] = {
                                "name": (
                                    track_values[name_idx].text
                                    if name_idx != -1
                                    else ""
                                ),
                                "artist": (
                                    track_values[artist_idx].text
                                    if artist_idx != -1
                                    else ""
                                ),
                                "album": (
                                    track_values[album_idx].text
                                    if album_idx != -1
                                    else ""
                                ),
                            }

            # Then find the specific playlist
            playlist_tracks = []
            for dict_elem in root.findall(".//dict"):
                keys = [k.text for k in dict_elem.findall("key")]
                values = dict_elem.findall("*")[1::2]  # Get all values

                if "Name" in keys:
                    name_idx = keys.index("Name")
                    if values[name_idx].text == playlist_name:
                        if "Playlist Items" in keys:
                            items_idx = keys.index("Playlist Items")
                            track_list = values[items_idx]

                            for track_item in track_list.findall("dict"):
                                track_id = track_item.find("integer").text
                                if track_id in tracks:
                                    playlist_tracks.append(tracks[track_id])

            return playlist_tracks
        except Exception as e:
            print(f"Error reading Apple Music Library: {str(e)}")
            return None

    def get_all_playlists(self):
        """
        Fetch all playlists and their tracks from Apple Music Library XML
        Returns a dictionary with playlist names as keys and track lists as values
        """
        try:
            tree = ET.parse(self.library_path)
            root = tree.getroot()

            # First get all tracks (reusing existing logic)
            tracks = {}
            for dict_elem in root.findall(".//dict"):
                keys = [k.text for k in dict_elem.findall("key")]
                if "Tracks" in keys:
                    tracks_dict = dict_elem.find("dict")
                    for track in tracks_dict.findall("dict"):
                        track_keys = [k.text for k in track.findall("key")]
                        track_values = track.findall("*")[1::2]  # Get all values

                        if "Track ID" in track_keys:
                            idx = track_keys.index("Track ID")
                            track_id = track_values[idx].text

                            name_idx = (
                                track_keys.index("Name") if "Name" in track_keys else -1
                            )
                            artist_idx = (
                                track_keys.index("Artist")
                                if "Artist" in track_keys
                                else -1
                            )
                            album_idx = (
                                track_keys.index("Album")
                                if "Album" in track_keys
                                else -1
                            )

                            tracks[track_id] = {
                                "name": (
                                    track_values[name_idx].text
                                    if name_idx != -1
                                    else ""
                                ),
                                "artist": (
                                    track_values[artist_idx].text
                                    if artist_idx != -1
                                    else ""
                                ),
                                "album": (
                                    track_values[album_idx].text
                                    if album_idx != -1
                                    else ""
                                ),
                            }

            # Then get all playlists
            playlists_dict = {}
            for dict_elem in root.findall(".//dict"):
                keys = [k.text for k in dict_elem.findall("key")]
                values = dict_elem.findall("*")[1::2]

                if "Name" in keys and "Playlist Items" in keys:
                    name_idx = keys.index("Name")
                    items_idx = keys.index("Playlist Items")

                    playlist_name = values[name_idx].text
                    track_list = values[items_idx]

                    playlist_tracks = []
                    for track_item in track_list.findall("dict"):
                        track_id = track_item.find("integer").text
                        if track_id in tracks:
                            playlist_tracks.append(tracks[track_id])

                    if playlist_tracks:  # Only add playlists that have tracks
                        playlists_dict[playlist_name] = playlist_tracks

            return playlists_dict
        except Exception as e:
            print(f"Error reading Apple Music Library: {str(e)}")
            return None
