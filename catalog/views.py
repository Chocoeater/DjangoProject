from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import Contact, Product


def home(request):
    last_products = Product.objects.order_by('-created_at')[:5]

    print('Последние 5 продуктов:')
    for product in last_products:
        print(product.id, product.product_name, product.created_at)
    return render(request, 'home.html')

def contacts(request):
    all_contacts = Contact.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone')
        massage = request.POST.get('massage')
        return HttpResponse(f'{name}, сообщение успешно отправлено!')
    return render(request, 'contacts.html', {'contacts': all_contacts})

