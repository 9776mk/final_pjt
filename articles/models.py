from django.db import models
from imagekit.models import ProcessedImageField
from django.contrib.auth import get_user_model
from accounts.models import User
from ckeditor.fields import RichTextField
# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=30)
    content = RichTextField(blank=True, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # image = ProcessedImageField()
    create_at = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, blank=True ,related_name="article_like")
    hits = models.PositiveIntegerField(default=0, verbose_name='조회수')
# Article의 이미지
class Image(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='article_images/')

class ArticleComment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)