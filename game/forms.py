from django import forms
from game.models import Game, PlayerGameInfo

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = {'number'}
        exclude = {'ongoing', 'players', 'final_tries'}

class TryForm(forms.ModelForm):
    class Meta:
        model = PlayerGameInfo
        fields = {'last_number'}
        exclude = {'player', 'game', 'tries', 'creator', 'announce'}