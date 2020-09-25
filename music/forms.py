import django.forms as forms
from django.forms import ModelForm, Form
from .models import Song
from .fields import ListTextWidget

class SongForm(ModelForm):
    class Meta:
        model = Song
        exclude = ['added_by']

    def __init__(self, *args, **kwargs):
        _data_list = kwargs.pop('data_list', None)
        super(SongForm, self).__init__(*args, **kwargs)

        # the "name" parameter will allow you to use the same widget more than once in the same
        # form, not setting this parameter differently will cuse all inputs display the
        # same list.
        if _data_list is not None:
            self.fields['artist'].widget = ListTextWidget(data_list=_data_list, name='data_list')
            self.fields['composer'].widget = ListTextWidget(data_list=_data_list, name='data_list')
            self.fields['conductor'].widget = ListTextWidget(data_list=_data_list, name='data_list')
            self.fields['orchestra'].widget = ListTextWidget(data_list=_data_list, name='data_list')
            self.fields['arranger'].widget = ListTextWidget(data_list=_data_list, name='data_list')

class SpotifyForm(Form):
    spotify_uri = forms.CharField(label="Spotify URI", max_length=100)
    
