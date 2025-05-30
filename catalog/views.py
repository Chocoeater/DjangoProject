from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from catalog.models import Contact, Product
from catalog.forms import ProductForm
from django.core.paginator import Paginator


def home(request):
    last_products = Product.objects.order_by('-created_at')[:5]
    print('Последние 5 продуктов:')
    for product in last_products:
        print(product.id, product.product_name, product.created_at)

    products = Product.objects.all()
    paginator = Paginator(products, 4) # задаем количество продуктов на главной
    number_of_page = request.GET.get('page') # получаем номер текущей страницы
    page_obj = paginator.get_page(number_of_page) # получаем страницу с товарами
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'home.html', context=context)

def contacts(request):
    all_contacts = Contact.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone')
        massage = request.POST.get('massage')
        return HttpResponse(f'{name}, сообщение успешно отправлено!')
    return render(request, 'contacts.html', {'contacts': all_contacts})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
    }

    return render(request, 'product_detail.html', context)


def success_add(request):
    return render(request, 'success_add.html')

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'success_add.html')
            # return HttpResponse("Продукт добавлен!")
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

