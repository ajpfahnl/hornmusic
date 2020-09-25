from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Playlist, Song
from .forms import SongForm, SpotifyForm
from .spotify import extract_track_details
from django.contrib.auth.models import User

def index(request):
    playlists = Playlist.objects.all()
    context = {'playlists': playlists}
    return render(request, "music/index.html", context)

@login_required
def contribute(request, spotify_uri):
    username = request.user.get_username()
    if request.method == "POST":
        form = SongForm(request.POST)
        if form.is_valid():
            new_song = form.save()
            return HttpResponseRedirect(reverse('music:index'))
    
    elif spotify_uri == "new":
        form = SongForm({"added_by": username})
        context = {'type': "new", 'form': form}
        return render(request, "music/contribute.html", context)
    
    else:
        track_info = extract_track_details(spotify_uri)
        artists = [item["name"] for item in track_info["artists"]]
        form = SongForm(data_list=artists, initial={"spotify_uri": spotify_uri, "title": track_info["name"], "added_by": username})
        context = {'type': "from_spotify", 'form': form, 'artists': track_info['artists'], 'name': track_info['name']}
        return render(request, "music/contribute.html", context)

@login_required
def edit_song(request, id):
    song = Song.objects.get(pk=id)
    if request.method == "POST":
        song.last_edit_by = request.user.get_username()
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            updated_song = form.save()
            return HttpResponseRedirect(reverse('music:index'))
    else:
        form = SongForm(instance=song)
        context = {'type': 'edit', 'form': form}
        return render(request, "music/contribute.html", context)

@login_required
def contribute_from_spotify(request):
    if request.method == "POST":
        form = SpotifyForm(request.POST)
        if form.is_valid():
            uri = form.cleaned_data["spotify_uri"]
            print(uri)
            return HttpResponseRedirect(reverse('music:contribute', args=(uri,)))
    else:
        form = SpotifyForm()
        context = {"form": form}
    return render(request, "music/contributespot.html", context)

def hornists(request):
    return render(request, "music/hornists.html")