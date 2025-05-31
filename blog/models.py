from django.db import models


# Create your models here.
class BlogRecord(models.Model):
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое")
    preview = models.ImageField(
        upload_to="blog/images", verbose_name="Превью", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    publication = models.BooleanField(
        default=True,
        verbose_name="Признак публикации",
    )
    number_of_views = models.IntegerField(
        verbose_name="Количество просмотров", default=0, blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "запись"
        verbose_name_plural = "записи"
        ordering = ["title", "content", "created_at", "publication"]
