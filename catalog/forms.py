from django import forms

from catalog.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'image_product', 'category', 'price']


    # ПОДСМОТРЕНО В ТЫРНЕТАХ
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # инициализация родительского класса ModelForm
        for field in self.fields: # проходимся по полям
            css_class = 'form-control' # назначаем класс по умолчанию (из бустрап)
            if isinstance(self.fields[field].widget, forms.Select):
                css_class = 'form-select' # если выпадающий список, то задаем соответствующий класс бустрап)
            elif isinstance(self.fields[field].widget, forms.ClearableFileInput):
                css_class = 'form-control' # если загрузка файла
            self.fields[field].widget.attrs['class'] = css_class # добавляем классы к базовой html форме
