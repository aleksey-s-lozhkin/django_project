from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import Contact, Product


def home(request):
    """Контроллер главной страницы с пагинацией"""

    # Получаем все продукты
    all_products = Product.objects.all().order_by('id')

    # Создаем пагинатор: 5 продуктов на страницу
    paginator = Paginator(all_products, 5)

    # Получаем номер страницы из GET-параметра
    page_number = request.GET.get('page')

    # Получаем объект страницы
    page_obj = paginator.get_page(page_number)

    # Передаем в контекст
    context = {
        'page_obj': page_obj,
        'latest_products': page_obj.object_list,  # для совместимости с вашим шаблоном
    }

    return render(request, 'home.html', context)


def contacts(request):
    """Контроллер страницы контактов"""

    # Получаем контактные данные из базы
    contact_info = Contact.objects.first()

    if request.method == 'POST':
        # Получаем данные из формы обратной связи
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        messages.success(request, 'Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')

        return redirect('/contacts/')

    context = {
        'contact': contact_info,
    }

    return render(request, 'contacts.html', context)


def product_details(request, pk):

    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
    }
    return render(request, 'product_details.html', context)
