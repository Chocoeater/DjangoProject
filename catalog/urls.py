from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import home, contacts, product_detail, add_product, success_add

app_name = CatalogConfig.name

urlpatterns = [
    path('home/', home, name='home'),
    path('contacts/', contacts, name='contacts'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
    path('success/', success_add, name='success_add'),
    path('add/', add_product, name='add_product'),
]
