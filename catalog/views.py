from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from catalog.models import Contact, Product


def home(request):
    last_products = Product.objects.order_by('-created_at')[:5]

    print('Последние 5 продуктов:')
    for product in last_products:
        print(product.id, product.product_name, product.created_at)

    products = Product.objects.all()
    context = {
        'products': products,
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