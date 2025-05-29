from django.db import models

# Create your models here.
class BlogRecord(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blog/images', verbose_name='Превью')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    publication = models.BooleanField(default=False, verbose_name='Признак публикации')
    number_of_views = models.IntegerField(verbose_name='Количество просмотров')