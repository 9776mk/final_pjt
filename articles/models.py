from django.db import models
from imagekit.models import ProcessedImageField
from django.contrib.auth import get_user_model
# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    image = ProcessedImageField()
class ArticleComment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    create_at = models.DateTimeField(null=True)