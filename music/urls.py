from django.urls import include, path
from . import views 
from allauth.account import views as allauth_views



urlpatterns = [
    path('', views.home, name='home'),

    path('accounts/', include('allauth.urls')),
   


    # Songs
    path('songs/', views.song_list, name='song_list'),
    path('songs/<int:pk>/', views.song_detail, name='song_detail'),


    # Artists
    path('artists/', views.artist_list, name='artist_list'),
    path('artists/<int:pk>/', views.artist_detail, name='artist_detail'),


    # Search
    path('search/', views.search, name='search'),


    # Playlists (login required for modifications)
    path('playlists/', views.playlist_list, name='playlist_list'),
    path('playlists/create/', views.playlist_create, name='playlist_create'),
    path('playlists/<int:pk>/', views.playlist_detail, name='playlist_detail'),
    path('playlists/<int:pk>/add/<int:song_id>/', views.playlist_add_song, name='playlist_add_song'),
    path('playlists/<int:pk>/remove/<int:song_id>/', views.playlist_remove_song, name='playlist_remove_song'),


   
]