from django.urls import path, include
from . import views

app_name = 'music'
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('contribute-song/', views.contribute_song, name='contribute_song'),
    path('spot-song/<str:spotify_uri>/', views.contribute_spotify_song, name='contribute_spotify_song'),
    path('contributespot/', views.contribute_from_spotify, name='contributespot'),
    path('<int:id>/edit/', views.edit_song, name='edit_song'),
    path('artists/', views.artists, name = 'artists'),
]