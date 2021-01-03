import django.forms as forms
from django.forms import ModelForm, Form, TextInput, Select
from .models import *
from .fields import ListTextWidget
from django.contrib import admin

class SongForm(ModelForm):
    album_text      = forms.CharField(widget=TextInput(), label="Album", required=False)
    artist_text     = forms.CharField(label="Artist", required=False)
    composer_text   = forms.CharField(label="Composer", required=False)
    conductor_text  = forms.CharField(label="Conductor", required=False)
    ensemble_text   = forms.CharField(label="Ensemble", required=False)
    arranger_text   = forms.CharField(label="Arranger", required=False)

    class Meta:
        model = Song
        fields = ['title', 
                  'album_text', 'artist_text', 'composer_text', 'conductor_text', 'ensemble_text', 'arranger_text',
                  'spotify_uri', 'youtube_url', 'other_url', 'playlists', 'notes']

    def __init__(self, *args, **kwargs):
        _data_list = kwargs.pop('data_list', None)
        super(SongForm, self).__init__(*args, **kwargs)

        # the "name" parameter will allow you to use the same widget more than once in the same
        # form, not setting this parameter differently will cuse all inputs display the
        # same list.
        if _data_list == None:
            _data_list = []
        self.fields['artist_text'].widget = ListTextWidget(data_list=_data_list, name='data_list')
        self.fields['composer_text'].widget = ListTextWidget(data_list=_data_list, name='data_list')
        self.fields['conductor_text'].widget = ListTextWidget(data_list=_data_list, name='data_list')
        self.fields['ensemble_text'].widget = ListTextWidget(data_list=_data_list, name='data_list')
        self.fields['arranger_text'].widget = ListTextWidget(data_list=_data_list, name='data_list')

class SongFormEdit(ModelForm):
    class Meta:
        model = Song
        fields = ['title', 
                  'album', 'artist', 'composer', 'conductor', 'ensemble', 'arranger',
                  'spotify_uri', 'youtube_url', 'other_url', 'playlists', 'notes']


class SpotifyURIForm(Form):
    spotify_uri = forms.CharField(label="Spotify URI", max_length=100)

class SpotifySongForm(ModelForm):
    album_text = forms.CharField(widget=TextInput(), label="Album", required=False)

    class Meta:
        model = Song
        fields = ['title', 'playlists', 'notes', 'spotify_uri']
        widgets = {
            'notes': forms.Textarea(attrs={'rows':2})
        }
    
    def __init__(self, *args, **kwargs):
        entities = kwargs.pop('entities', [])
        super(SpotifySongForm, self).__init__(*args, **kwargs)
        for i, entity in enumerate(entities):
            self.fields[f'entity_{entity}'] = forms.MultipleChoiceField(label=entity, choices=ROLE_OPTIONS, widget = forms.CheckboxSelectMultiple, required=False)

