from catalog.models import Category, Product


class ProductService:

    @staticmethod
    def category_filter(queryset, category_id: int):
        """
        Возвращает продукты заданной категории
        :param category: категория продукта
        :return: список продуктов-объектов
        """
        return queryset.filter(category_id=category_id)
