from django import forms
from .models import *
from django.forms import Textarea


class StudyForm(forms.ModelForm):
    class Meta:
        model = Study
        exclude = [
            "host_user",
            "is_closed",
        ]


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = [
            "title",
            "category",
            "problem_number",
            "content",
        ]
        widgets = {
            "content": Textarea(
                attrs={
                    "style": "width: 100%; resize: none; outline: none; border: none; padding: 22px;",
                }
            ),
        }


class BoardCommentForm(forms.ModelForm):
    class Meta:
        model = BoardComment
        fields = [
            "content",
        ]
