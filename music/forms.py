import django.forms as forms
from django.forms import ModelForm, Form
from .models import Song

class SongForm(ModelForm):
    class Meta:
        model = Song
        fields = '__all__'

class SongFormPrefill(ModelForm):
    class Meta:
        model = Song
        fields = '__all__'

class SpotifyForm(Form):
    spotify_uri = forms.CharField(label="Spotify URI", max_length=100)
    
