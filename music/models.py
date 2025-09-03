from django.db import models
from django.contrib.auth.models import User


class Artist(models.Model):
    name = models.CharField(max_length=120, unique=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='artists/', blank=True, null=True)


def __str__(self):
    return self.name


class Song(models.Model):
    title = models.CharField(max_length=200)
    audio_file = models.FileField(upload_to='songs/') # mp3/m4a/wav/ogg, etc.
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    artists = models.ManyToManyField(Artist, related_name='songs')
    duration_seconds = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return self.title


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    name = models.CharField(max_length=120)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return f"{self.name} — {self.user.username}"


class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='items')
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)


class Meta:
    unique_together = ('playlist', 'song')
    ordering = ('order', 'id')


def __str__(self):
    return f"{self.playlist.name}: {self.song.title}"