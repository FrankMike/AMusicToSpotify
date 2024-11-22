import xml.etree.ElementTree as ET
import os


class AppleMusicClient:
    def __init__(self):
        # Default iTunes Library XML location on macOS
        self.library_path = os.path.expanduser(
            "~/Music/iTunes/iTunes Music Library.xml"
        )
        # For newer versions of macOS, might be in:
        # ~/Music/Music/Library.xml

    def get_playlist(self, playlist_name):
        """
        Fetch a playlist and its tracks from iTunes Library XML
        """
        try:
            tree = ET.parse(self.library_path)
            root = tree.getroot()

            tracks = {}
            playlists = []

            # First, get all tracks
            for dict_elem in root.findall(".//dict"):
                if dict_elem.find("key[.='Tracks']") is not None:
                    tracks_dict = dict_elem.find("dict")
                    for track in tracks_dict.findall("dict"):
                        track_id = track.findtext(
                            "key[.='Track ID']/following-sibling::integer[1]"
                        )
                        if track_id:
                            tracks[track_id] = {
                                "name": track.findtext(
                                    "key[.='Name']/following-sibling::string[1]"
                                ),
                                "artist": track.findtext(
                                    "key[.='Artist']/following-sibling::string[1]"
                                ),
                                "album": track.findtext(
                                    "key[.='Album']/following-sibling::string[1]"
                                ),
                            }

            # Then find the specific playlist
            playlist_tracks = []
            for dict_elem in root.findall(".//dict"):
                if dict_elem.find("key[.='Name']") is not None:
                    name = dict_elem.findtext(
                        "key[.='Name']/following-sibling::string[1]"
                    )
                    if name == playlist_name:
                        track_list = dict_elem.find(
                            "key[.='Playlist Items']/following-sibling::array[1]"
                        )
                        if track_list is not None:
                            for track_item in track_list.findall("dict"):
                                track_id = track_item.findtext(
                                    "key[.='Track ID']/following-sibling::integer[1]"
                                )
                                if track_id in tracks:
                                    playlist_tracks.append(tracks[track_id])

            return playlist_tracks
        except Exception as e:
            print(f"Error reading iTunes Library: {e}")
            return None
