from django.contrib import messages
from django.shortcuts import redirect, render


def home(request):
    return render(request, 'home.html')


def contacts(request):
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        messages.success(request, 'Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')

        return redirect('/contacts/')

    return render(request, 'contacts.html')
