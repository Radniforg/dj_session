from django import forms

class GameForm(forms.Form):
    number = forms.IntegerField(label='')