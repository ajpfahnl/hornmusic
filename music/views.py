from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import SongForm, SpotifyURIForm, SpotifySongForm, SongFormEdit
from .spotify import extract_track_details
from django.contrib.auth.models import User

def index(request):
    playlists = Playlist.objects.all()
    context = {'playlists': playlists}
    return render(request, "music/index.html", context)

@login_required
def contribute_entity(request):
    username = request.user.get_username()
    if request.method == "POST":
        form = EntityForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('music:index'))
    else:
        form = SongForm()

@login_required
def contribute_song(request, spotify_uri=None):
    if request.method == "POST":
        form = SongFormEdit(request.POST)
        if form.is_valid():
            new_song = form.save()
            return HttpResponseRedirect(reverse('music:index'))
        else:
            context = {'form': form}
    
    else:
        form = SongFormEdit({"added_by": request.user.get_username()})
        context = {'type': "new", 'form': form}
    return render(request, "music/contribute_song.html", context)

@login_required
def edit_song(request, id):
    song = Song.objects.get(pk=id)
    if request.method == "POST":
        song.last_edit_by = request.user.get_username()
        form = SongFormEdit(request.POST, instance=song)
        if form.is_valid():
            updated_song = form.save()
            return HttpResponseRedirect(reverse('music:index'))
    else:
        form = SongFormEdit(instance=song)
        context = {'type': 'edit', 'form': form}
        return render(request, "music/contribute_song.html", context)

@login_required
def contribute_spotify_song(request, spotify_uri):
    track_info = extract_track_details(spotify_uri)
    entities = [item["name"] for item in track_info["artists"]]
    if request.method == 'POST':
        form = SpotifySongForm(request.POST, entities=entities)
        if form.is_valid():
            new_song = form.save()
            # Album title
            if form.cleaned_data['album_text']:
                album_text = form.cleaned_data['album_text']
                album_objects = Album.objects.filter(name__exact=album_text)
                if album_objects:
                    new_song.album = album_objects[0]
                else:
                    new_song.album = Album.objects.create(name=album_text)

            # Entities parsing
            entities = []
            for field in form.cleaned_data:
                if field.split('_')[0] == "entity":
                    entities.append(field)
            for entity in entities:
                roles = form.cleaned_data[entity]
                entity = '_'.join(entity.split('_')[1:])
                for role in roles:
                    entity_objects = Entity.objects.filter(name__exact=entity)
                    role_str = get_role_str(role)
                    if len(entity_objects) == 0:
                        new_song_role_create = getattr(getattr(new_song, role_str+'s'), 'create')
                        new_song_role_create(name=entity)
                    else:
                        new_song_role_add = getattr(getattr(new_song, role_str+'s'), 'add')
                        new_song_role_add(entity_objects[0])
            new_song.save()
            return HttpResponseRedirect(reverse('music:index'))

    else:
        form = SpotifySongForm(entities=entities, 
                               initial={"spotify_uri": spotify_uri, 
                                        "title": track_info["name"], 
                                        "added_by": request.user.get_username(), 
                                        "album_text": track_info["album_name"]})
    
    context = {'type': "from_spotify", 'form': form}
    return render(request, "music/contribute_song.html", context)

@login_required
def contribute_from_spotify(request):
    if request.method == "POST":
        form = SpotifyURIForm(request.POST)
        if form.is_valid():
            uri = form.cleaned_data["spotify_uri"]
            if not Song.objects.filter(spotify_uri=uri):
                return HttpResponseRedirect(reverse('music:contribute_spotify_song', args=(uri,)))
            else:
                context = {"form": form, "uri_used": True}
    else:
        form = SpotifyURIForm()
        context = {"form": form}

    return render(request, "music/contributespot.html", context)

def artists(request):
    return render(request, "music/artists.html")