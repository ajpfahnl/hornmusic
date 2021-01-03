from django.db import models

SHORT_LEN = 150
URI_LEN = 200

ARTIST = 'A'
COMPOSER = 'C'
CONDUCTOR = 'D'
ENSEMBLE = 'E'
ARRANGER = 'R'

ROLE_OPTIONS = [
    (ARTIST, 'artist'),
    (COMPOSER, 'composer'),
    (CONDUCTOR, 'conductor'),
    (ENSEMBLE, 'ensemble'),
    (ARRANGER, 'arranger'),
]

def get_role_str(role):
    for role_tup in ROLE_OPTIONS:
        if role_tup[0] == role:
            return role_tup[1]
    return None

class Album(models.Model):
    name = models.CharField(max_length=SHORT_LEN)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Entity(models.Model):
    name = models.CharField(max_length=SHORT_LEN)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class EntityAlias(models.Model):
    alias = models.CharField(max_length=SHORT_LEN)
    entity = models.ManyToManyField(Entity)
    def __str__(self):
        return self.alias


class Playlist(models.Model):
    title = models.CharField(max_length=SHORT_LEN)
    description = models.TextField(blank=True)
    added_by = models.CharField(max_length=SHORT_LEN, default="admin")
    def __str__(self):
        return self.title
    
class Song(models.Model):
    title           = models.CharField(max_length=SHORT_LEN)
    album           = models.ForeignKey(Album, on_delete=models.CASCADE, blank=True, null=True)
    artist          = models.ManyToManyField(Entity, blank=True, related_name="artist_song_set")
    composer        = models.ManyToManyField(Entity, blank=True, related_name="composer_song_set")
    arranger        = models.ManyToManyField(Entity, blank=True, related_name="arranger_song_set")
    conductor       = models.ManyToManyField(Entity, blank=True, related_name="conductor_song_set")
    ensemble        = models.ManyToManyField(Entity, blank=True, related_name="ensemble_song_set")
    spotify_uri     = models.CharField("Spotify URI", max_length=URI_LEN, blank=True)
    youtube_url     = models.CharField("YouTube URL", max_length=URI_LEN, blank=True)
    other_url       = models.CharField("Other URL", max_length=URI_LEN, blank=True)
    playlists       = models.ManyToManyField(Playlist)
    added_by        = models.CharField(max_length=SHORT_LEN, default="admin") # auto-generated based on user
    last_edit_by    = models.CharField(max_length=SHORT_LEN, default="admin") # auto-generated based on user
    notes           = models.TextField(blank=True)
    def __str__(self):
        return self.title
    def get_id(self):
        return self.spotify_uri.split(':')[-1]