from django.db import models


# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['category_name', ]


class Product(models.Model):
    product_name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    image_product = models.ImageField(upload_to='catalog/images', verbose_name='Изображение', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    price = models.FloatField(verbose_name='Стоимость')
    created_at = models.DateTimeField(verbose_name='Дата создания')
    updated_at = models.DateTimeField(verbose_name='Дата изменения')

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['product_name', 'price', ]
