from django import forms
from .models import Player


class SquadPicker(forms.Form):
    GK = forms.ModelChoiceField(queryset=Player.objects.filter(position=1).order_by('-value'),
                                label='Choose a goalkeeper:',
                                widget=forms.Select(attrs={'style': 'width:300px'}))
    DEF = forms.ModelMultipleChoiceField(queryset=Player.objects.filter(position=2).order_by('-value'),
                                         label='Choose four defenders:',
                                         help_text='On a computer, use CTRL/CMD + left click to select multiple choices below',
                                         widget=forms.SelectMultiple(attrs={'style': 'width:300px'}))
    MID = forms.ModelMultipleChoiceField(queryset=Player.objects.filter(position=3).order_by('-value'),
                                         label='Choose four midfielders:',
                                         widget=forms.SelectMultiple(attrs={'style': 'width:300px'}))
    FWD = forms.ModelMultipleChoiceField(queryset=Player.objects.filter(position=4).order_by('-value'),
                                         label='Choose two forwards:',
                                         widget=forms.SelectMultiple(
                                             attrs={'style': 'width:300px', 'draggable': "true"}))
    Choices = ((1, 'One sub based on tweets'),
               (0, 'One sub based on performance'),)
    choice = forms.ChoiceField(choices=Choices, label='Choose substitution type:',
                               widget=forms.Select(attrs={'style': 'width:300px'}))
