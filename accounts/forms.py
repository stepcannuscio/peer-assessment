from django import forms
from .models import *

class CreateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer', 'score', 'question']

    # def clean(self):
