from django.contrib import messages
from django.shortcuts import redirect, render
from catalog.models import Product, Contact


def home(request):
    """Контроллер главной страницы с выводом последних 5 продуктов в консоль"""

    # Выборка последних 5 созданных продуктов
    latest_products = Product.objects.order_by('-created_at')[:5]

    # Вывод в консоль
    print("=" * 50)
    print("ПОСЛЕДНИЕ 5 СОЗДАННЫХ ПРОДУКТОВ:")
    print("=" * 50)
    for product in latest_products:
        print(f"• {product.name}")
        print(f"  Цена: {product.price} руб.")
        print(f"  Категория: {product.category.name if product.category else 'Без категории'}")
        print(f"  Создан: {product.created_at}")
        print("-" * 30)
    print(f"Всего показано: {len(latest_products)} продуктов")
    print("=" * 50)

    # Передаем последние продукты в шаблон
    context = {
        'latest_products': latest_products,
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