from django.shortcuts import render
from django.core.exceptions import MultipleObjectsReturned

from game.forms import GameForm, TryForm
from game.models import Player, Game, PlayerGameInfo


def show_home(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    current_player = request.session.get('player', 'new')
    if current_player is 'new':
        Player.objects.create(session_id=request.session.session_key)
        request.session['player'] = 'old'
    player = Player.objects.get(session_id=request.session.session_key)
    if not Game.objects.filter(ongoing=True):
        if not player.playergameinfo_set.filter(announce=False):
            # Нет активных игр и все результаты для игрока были объявлены: создание новой игры
            if request.method == 'POST':
                form = GameForm(request.POST)
                if form.is_valid():
                    game_save = form.save(commit=False)
                    game_save.players.add(player)
                    game_save.playergameinfo_set.create(player=player, creator=True)
                    game_save.save()
                    return render(request,
                                  'input.html')
            else:
                form = GameForm()
                return render(request, 'home.html', context={'form': form})
        else:
            #если нет активных игр, но результаты прошлых игр игроку не объявлялись
            current_game = player.playergameinfo_set.filter(announce=False)[0]
            game_id = current_game.game
            tries = game_id.final_tries
            creator = current_game.creator
            current_game.save()
            return render(request, 'result.html', context={
                'tries': tries, 'creator': creator})
    else:
        #если есть активная игра
        try:
            game = Game.objects.get(ongoing=True)
        except MultipleObjectsReturned:
            game = Game.objects.filter(ongoing=True)[0]
        if not game.playergameinfo_set.filter(creator=False):
            #Проверяет, является ли игрок создателем активной игры
            return render(request,
                          'input.html')
        else:
            if request.method == 'POST':
                form = TryForm(request.POST)
                if form.is_valid():
                    game_save = form.save(commit=False)
                    game_save.save()
                    if game_save.last_number == game.number:
                        #Если угадал
                        game.final_tries = game_save.tries
                        game.ongoing = False
                        game_save.announce = True
                        game_save.save()
                        game.save()
                        return render(request, 'success.html',
                                      context={'tries': game.final_tries,
                                               'number': game.number})
                    else:
                        #Если не угадал
                        game_save.tries += 1
                        game_save.save()
                        return render(request, 'again.html',
                                      context={'number': game_save.last_number,
                                               'form': form})
            form = TryForm()
            return render(
                request,
                'again.html',
                context={'form': form}
            )





