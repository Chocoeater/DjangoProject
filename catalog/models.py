from django.db import models

# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = [
            "category_name",
        ]


class Product(models.Model):
    product_name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание")
    image_product = models.ImageField(
        upload_to="catalog/images", verbose_name="Изображение", blank=True, null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
    )
    price = models.FloatField(verbose_name="Стоимость")
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)
    status = models.BooleanField(default=False, verbose_name="Статус публикации")
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Владелец",
    )

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = [
            "product_name",
            "price",
        ]
        permissions = [
            ("can_unpublish_product", "Может менять статус продукта"),
        ]


class Contact(models.Model):
    contact_name = models.CharField(max_length=150, verbose_name="Имя контакта")
    phone_number = models.CharField(max_length=18, verbose_name="Номер телефона")

    def __str__(self):
        return f"{self.contact_name} - {self.phone_number}"

    class Meta:
        verbose_name = "контакт"
        verbose_name_plural = "контакты"
