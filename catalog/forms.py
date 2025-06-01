from django import forms
from django.conf import settings

from catalog.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'image_product', 'category', 'price']

    # ПОДСМОТРЕНО В ТЫРНЕТАХ
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # инициализация родительского класса ModelForm
        for field in self.fields:  # проходимся по полям
            css_class = 'form-control'  # назначаем класс по умолчанию (из бустрап)
            if isinstance(self.fields[field].widget, forms.Select):
                css_class = 'form-select'  # если выпадающий список, то задаем соответствующий класс бустрап)
            elif isinstance(self.fields[field].widget, forms.ClearableFileInput):
                css_class = 'form-control'  # если загрузка файла
            self.fields[field].widget.attrs['class'] = css_class  # добавляем классы к базовой html форме

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError('Цена не может иметь отрицательное значение')
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Размер файла не должен превышать 5 мб')

            valid_types = ['image/jpeg', 'image/png']
            if image.content_type not in valid_types:
                raise forms.ValidationError('Файл должен быть в формате JPEG или PNG')

        return image

    def clean(self):
        cleaned_data = super().clean()
        product_name = cleaned_data.get('product_name', '').lower()
        description = cleaned_data.get('description', '').lower()

        forbidden_words = getattr(settings, 'FORBIDDEN_WORDS', [])
        found_words = []

        for word in forbidden_words:
            if word in product_name or word in description:
                found_words.append(word)

        if found_words:
            raise forms.ValidationError(f'Обнаружены запрещенные слова: {", ".join(found_words)}')
