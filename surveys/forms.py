from django import forms
from .models import *


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = '__all__'