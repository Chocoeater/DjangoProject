from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'home.html')

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone')
        massage = request.POST.get('massage')

        return HttpResponse(f'{name}, сообщение успешно отправлено!')
    return render(request, 'contacts.html')