from django import forms
from game.models import Game, PlayerGameInfo

class GameForm(forms.Form):
    class Meta:
        model = Game
        fields = {'number'}

class TryForm(forms.Form):
    class Meta:
        model = PlayerGameInfo
        fields = {'last_number'}
        exclude = {'player', 'game', 'tries', 'creator', 'announce'}