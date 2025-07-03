from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (ContactSuccessView, ContactView, ProductCreateView,
                           ProductDeleteView, ProductDetailView,
                           ProductListView, ProductUpdateView, success_add)

app_name = CatalogConfig.name

urlpatterns = [
    path("contacts/", ContactView.as_view(), name="contacts"),
    path("contacts/success", ContactSuccessView.as_view(), name="success_contact"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("success/", success_add, name="success_add"),
    path("add/", ProductCreateView.as_view(), name="create_product"),
    path("", ProductListView.as_view(), name="product_list"),
    path(
        "product/update/<int:pk>/", ProductUpdateView.as_view(), name="product_update"
    ),
    path(
        "product/delete/<int:pk>/", ProductDeleteView.as_view(), name="product_delete"
    ),
]
