from django.urls import path
from . import views

app_name = 'music'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:id>/contribute/', views.contribute, name='contribute'),
    path('contributespot/', views.contribute_from_spotify, name='contributespot'),
    path('hornists/', views.hornists, name = 'hornists'),
]