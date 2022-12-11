from django import forms

from .models import Article, Image, ArticleComment
from django.forms import ModelForm, Textarea


class articleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "title",
            "content",
            "category",
            # 'image',
        ]
        widgets = {
            "content": Textarea(
                attrs={
                    "style": "width: 100%; resize: none; outline: none; border: none; padding: 22px;",
                }
            ),
        }


class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = [
            "content",
        ]


# ClearableFileInput으로 여러 장의 image를 입력 받을 수 있음
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["image"]
        widgets = {"image": forms.ClearableFileInput(attrs={"multiple": True})}
