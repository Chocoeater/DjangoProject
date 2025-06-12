from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q

from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Contact, Product

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'product_update.html'
    context_object_name = 'product'

    def get_success_url(self):
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})

    def get_form_class(self):
        user = self.request.user
        if user.has_perm('catalog.change_product') or user == self.object.owner:
            return ProductForm
        if user.has_perm('catalog.can_unpublish_product'):
            return ProductModeratorForm
        raise PermissionDenied

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_delete.html'
    context_object_name = 'product'
    success_url = reverse_lazy('catalog:product_list')

    # def get_queryset(self):
    #     return Product.objects.filter(owner=self.request.user) # 404 не устраивает

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise PermissionDenied
        return obj


class ProductListView(ListView):
    model = Product
    template_name = "home.html"
    context_object_name = "products"
    paginate_by = 4

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser or user.is_staff or user.groups.filter(name='Модераторы').exists():
                return Product.objects.all()
            else:
                return Product.objects.filter(
                    Q(status=True) | Q(owner=user)
                ).distinct()
        else:
            return Product.objects.filter(status=True)


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
