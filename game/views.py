from django.shortcuts import render
from django.core.exceptions import MultipleObjectsReturned

from game.forms import GameForm, TryForm
from game.models import Player, Game, PlayerGameInfo


def show_home(request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    current_player = request.session.get('player', 'new')
    if current_player == 'new':
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
                    game_save.save()
                    game_save.players.add(player)
                    game_save.save()
                    creator = game_save.playergameinfo_set.filter(player=player)[0]
                    creator.creator = True
                    creator.save()
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
            current_game.announce = True
            current_game.save()
            return render(request, 'result.html', context={
                'tries': tries, 'creator': creator,
                'number': game_id.number})
    else:
        #если есть активная игра
        game = Game.objects.filter(ongoing=True).first()
        if not player.games.filter(ongoing=True):
            player.games.add(game)
            player.save()
        if not game.playergameinfo_set.filter(creator=False):
            #Проверяет, является ли игрок создателем активной игры
            return render(request,
                          'input.html',
                          context={'key': request.session.session_key})
        else:
            current = player.playergameinfo_set.get(game=game)
            if request.method == 'POST':
                form = TryForm(request.POST)
                if form.is_valid():
                    game_save = form.save(commit=False)
                    if game_save.last_number == game.number:
                        #Если угадал
                        game.final_tries = current.tries + 1
                        game.ongoing = False
                        current.announce = True
                        current.last_number = game_save.last_number
                        current.save()
                        game.save()
                        return render(request, 'success.html',
                                      context={'tries': game.final_tries,
                                               'number': game.number})
                    else:
                        #Если не угадал
                        current.last_number = game_save.last_number
                        current.tries += 1
                        current.save()
                        return render(request, 'again.html',
                                      context={'number': current.last_number,
                                               'original': game.number,
                                               'form': form,
                                               'tries': current.tries})
            form = TryForm()
            tries = current.tries
            original = game.number
            number = current.last_number
            return render(
                request,
                'again.html',
                context={'form': form,
                         'original': original,
                         'tries': tries,
                         'number': number}
            )





