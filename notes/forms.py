from .models import *
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ("to_id","title", "content")
        labels = {
            "to_id": "받는 사람 (ID)",
            "title": "제목",
            "content": "내용",
        }

    def clean_to_id(self):
        to_id = self.cleaned_data["to_id"]
        if not len(get_user_model().objects.filter(username=self.cleaned_data["to_id"])):
            raise ValidationError("존재하지 않는 아이디입니다.")
        return to_id

class NotesReplyForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ("title", "content")
        labels = {
            "title": "제목",
            "content": "내용",
        }