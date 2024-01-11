class Song:
    def __init__(self, title, artists, album, duration):
        self.title = title
        self.artists = artists
        self.album = album
        self.duration = duration
    

    
    def __str__(self):
        track_artists = ""
        for artist in self.artists:
            current_artist = artist.name
            last_artist = self.artists[-1].name
        if current_artist == last_artist:
            track_artists += f" {current_artist}"
        else:
            track_artists += f" {current_artist},"
        return f"{self.title} by{track_artists}"