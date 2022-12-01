from .models import *
from django import forms


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ("to_user","title", "content")
        labels = {
            "to_user":"받는사람",
            "title": "제목",
            "content": "내용",
        }