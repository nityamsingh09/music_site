from django.contrib import admin
from .models import Artist, Song, Playlist, PlaylistSong


class PlaylistSongInline(admin.TabularInline):
    model = PlaylistSong
    extra = 0


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'artists__name')
    filter_horizontal = ('artists',)


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_public', 'created_at')
    search_fields = ('name', 'user__username')
    inlines = [PlaylistSongInline]