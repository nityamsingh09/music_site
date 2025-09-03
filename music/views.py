from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from django.shortcuts import render
from .models import Artist

def artist_list(request):
    artists = Artist.objects.all()
    return render(request, 'music/artist_list.html', {'artists': artists})




from .models import Song, Artist, Playlist, PlaylistSong

def home(request):
    songs = Song.objects.select_related().prefetch_related('artists').order_by('-created_at')[:20]
    return render(request, 'music/home.html', {'songs': songs})



def song_list(request):
    songs = Song.objects.prefetch_related('artists').order_by('-created_at')
    return render(request, 'music/song_list.html', {'songs': songs})


def song_detail(request, pk):
    song = get_object_or_404(Song.objects.prefetch_related('artists'), pk=pk)
    return render(request, 'music/song_detail.html', {'song': song})

def artist_detail(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    songs = artist.songs.all().order_by('-created_at')
    return render(request, 'music/artist_detail.html', {'artist': artist, 'songs': songs})

def search(request):
    q = request.GET.get('q', '').strip()
    song_results = artist_results = []
    if q:
        song_results = Song.objects.filter(
        Q(title__icontains=q) | Q(artists__name__icontains=q)
        ).distinct().prefetch_related('artists')
        artist_results = Artist.objects.filter(name__icontains=q)
        context = {'q': q, 'song_results': song_results, 'artist_results': artist_results}
        return render(request, 'music/search.html', context)
    
def _owns_playlist(user, playlist):
    return playlist.user_id == user.id

@login_required
def playlist_list(request):
    playlists = Playlist.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'music/playlist_list.html', {'playlists': playlists})


@login_required
def playlist_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip() or 'New Playlist'
        pl = Playlist.objects.create(user=request.user, name=name)
        return redirect('playlist_detail', pk=pl.pk)
    return render(request, 'music/playlist_create.html')


@login_required
def playlist_detail(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk)
    if not _owns_playlist(request.user, playlist):
        return HttpResponseForbidden('Not your playlist')
    items = playlist.items.select_related('song').prefetch_related('song__artists')
    return render(request, 'music/playlist_detail.html', {'playlist': playlist, 'items': items})


@login_required
def playlist_add_song(request, pk, song_id):
    playlist = get_object_or_404(Playlist, pk=pk)
    if not _owns_playlist(request.user, playlist):
        return HttpResponseForbidden('Not your playlist')
    song = get_object_or_404(Song, pk=song_id)
    order = playlist.items.count()
    PlaylistSong.objects.get_or_create(playlist=playlist, song=song, defaults={'order': order})
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'ok': True})
    return redirect('playlist_detail', pk=pk)


@login_required
def playlist_remove_song(request, pk, song_id):
    playlist = get_object_or_404(Playlist, pk=pk)
    if not _owns_playlist(request.user, playlist):
        return HttpResponseForbidden('Not your playlist')
    PlaylistSong.objects.filter(playlist=playlist, song_id=song_id).delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'ok': True})
    return redirect('playlist_detail', pk=pk)