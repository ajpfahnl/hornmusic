from django.contrib import admin
from .models import Song, Playlist, Entity, EntityAlias, Album

admin.site.register(Album)
admin.site.register(Entity)
admin.site.register(EntityAlias)
admin.site.register(Song)
admin.site.register(Playlist)