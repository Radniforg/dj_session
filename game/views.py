from django.shortcuts import render

from game.forms import GameForm
from game.models import Game


def show_home(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,
                          'success.html')

    return render(
        request,
        'home.html',
        context = {'form': form}
    )
