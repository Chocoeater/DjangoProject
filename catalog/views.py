from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from catalog.models import Contact, Product
from catalog.forms import ProductForm, ContactForm
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse


class ProductListView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'
    paginate_by = 4

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

class ProductCreateView(CreateView):
    model = Product
    template_name = 'add_product.html'
    form_class = ProductForm
    success_url = reverse_lazy('catalog:success_add')

class ContactView(View):
    template_name = 'contacts.html'

    def get(self, request):
        contacts = Contact.objects.all()
        return render(request, self.template_name, {'contacts': contacts})

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        print(name, phone, message)

        messages.success(request, f'{name}, сообщение отправлено! Скоро свяжемся!')

        return redirect('catalog:success_contact')

class ContactSuccessView(View):
    template_name = 'success_send_message.html'

    def get(self, request):
        return render(request, self.template_name)

def success_add(request):
    return render(request, 'success_add.html')



