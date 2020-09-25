from django.db import models

class Playlist(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300, blank=True)
    added_by = models.CharField(max_length=150, default="admin")
    def __str__(self):
        return self.title
    
class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=50, blank=True)
    composer = models.CharField(max_length=50, blank=True)
    arranger = models.CharField(max_length=50, blank=True)
    conductor = models.CharField(max_length=50, blank=True)
    orchestra = models.CharField(max_length=50, blank=True)
    spotify_uri = models.CharField("Spotify URI", max_length=200, blank=True)
    youtube_url = models.CharField("YouTube URL", max_length=200, blank=True)
    other_url = models.CharField("Other URL", max_length=200, blank=True)
    playlists = models.ManyToManyField(Playlist)
    added_by = models.CharField(max_length=150, default="admin")
    notes = models.CharField(max_length=300, blank=True)
    def __str__(self):
        return self.title
    def get_id(self):
        return self.spotify_uri.split(':')[-1]

    # title_text, artist_text, composer_text, conductor_text, orchestra_text, uri_spotify_text