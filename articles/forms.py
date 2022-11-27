from django import forms
from .models import Article, Image

class articleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title',
            'content',
            # 'image',
        ]


# ClearableFileInput으로 여러 장의 image를 입력 받을 수 있음
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True})
        }