from django import forms
from .models import Article,ArticleComment

class articleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title',
            'content',
            # 'image',
        ]

class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = [  
            'content',
        ]