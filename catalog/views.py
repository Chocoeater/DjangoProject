from asyncio import timeout
from unicodedata import category

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Category, Contact, Product
from catalog.services import ProductService


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = "product_update.html"
    context_object_name = "product"

    def get_success_url(self):
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})

    def get_form_class(self):
        user = self.request.user
        if user.has_perm("catalog.change_product") or user == self.object.owner:
            return ProductForm
        if user.has_perm("catalog.can_unpublish_product"):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "product_delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("catalog:product_list")

    # def get_queryset(self):
    #     return Product.objects.filter(owner=self.request.user) # 404 не устраивает

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if (
            obj.owner != self.request.user
            or not self.request.user.is_staff
            or not self.request.user.is_superuser
            or not self.request.user.groups.filter(name="Модераторы").exists()
        ):
            raise PermissionDenied
        return obj


class ProductListView(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "products"
    paginate_by = 4

    def get_queryset(self):
        user = self.request.user
        category_id = self.request.GET.get("category_id")

        cache_key = f'prod_qs_user_{user.pk if user.is_authenticated else "anonim"}_cat_{category_id if category_id else "all"}'

        queryset = cache.get(cache_key)
        if queryset:
            return queryset

        if user.is_authenticated:
            if (
                user.is_superuser
                or user.is_staff
                or user.groups.filter(name="Модераторы").exists()
            ):
                queryset = Product.objects.all()
            else:
                queryset = Product.objects.filter(
                    Q(status=True) | Q(owner=user)
                ).distinct()
        else:
            queryset = Product.objects.filter(status=True)

        if category_id:
            try:
                category_id = int(category_id)
                queryset = ProductService.category_filter(queryset, category_id)
            except ValueError:
                pass

        cache.set(cache_key, queryset, 60 * 5)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        try:
            context["current_category_id"] = int(self.request.GET.get("category_id"))
        except (TypeError, ValueError):
            context["current_category_id"] = None
        return context


@method_decorator(cache_page(60 * 15), name="dispatch")
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "add_product.html"
    success_url = reverse_lazy("catalog:success_add")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ContactView(LoginRequiredMixin, View):
    template_name = "contacts.html"

    def get(self, request):
        contacts = Contact.objects.all()
        return render(request, self.template_name, {"contacts": contacts})

    def post(self, request):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        print(name, phone, message)

        messages.success(request, f"{name}, сообщение отправлено! Скоро свяжемся!")

        return redirect("catalog:success_contact")


class ContactSuccessView(LoginRequiredMixin, View):
    template_name = "success_send_message.html"

    def get(self, request):
        return render(request, self.template_name)


def success_add(request):
    return render(request, "success_add.html")
