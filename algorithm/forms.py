from django import forms
from .models import Tag
from .widgets import CustomCheckboxSelectMultiple


class PostSearchForm(forms.Form):
    """게시글 검색 폼"""

    key_word = forms.CharField(
        label="검색키워드",
        required=False,
    )

    tags = forms.ModelMultipleChoiceField(
        label="태그범위축소검색",
        required=False,
        queryset=Tag.objects.order_by("name"),
        widget=CustomCheckboxSelectMultiple,
    )
