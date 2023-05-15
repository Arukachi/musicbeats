from django.shortcuts import render
from django.db.models import Case, When, F
from django.contrib.auth.models import User
from musicbeats.models import Song
from musicbeats.models import Playlist, History


def index(request):
    song = Song.objects.all()[0:4]

    if request.user.is_authenticated:
        pl = Playlist.objects.filter(user=request.user)
        his = History.objects.filter(user=request.user)
        idsp = []
        idsh = []
        for i in pl:
            idsp.append(i.video_id)
        for i in his:
            idsh.append(i.music_id)

        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(idsp)])
        pr = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(idsh)])
        playlist = Song.objects.filter(song_id__in=idsp).order_by(preserved)
        playlist = reversed(playlist)
        history = Song.objects.filter(song_id__in=idsh).order_by(pr)
        history = reversed(history)

    else:
        playlist = Song.objects.all()[0:4]
        history = Song.objects.all()[0:4]

    return render(request, 'index.html', {'song': song, 'playlist': playlist, 'history': history})
