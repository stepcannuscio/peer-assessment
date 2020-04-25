from django import forms
from .models import *

class CreateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']

class AddStudentForm(forms.ModelForm):
    class Meta:
        model = Team_Enrollment
        fields = ['user', 'team']
