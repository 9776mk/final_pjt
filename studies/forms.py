from django import forms
from .models import *

class StudyForm(forms.ModelForm):
    class Meta:
        model = Study
        exclude = ['host_user', 'is_closed',]