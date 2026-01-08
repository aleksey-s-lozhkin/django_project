from django.contrib import admin
from .models import Product, Category

"""
Административная конфигурация для приложений каталога:
- Регистрирует модели Product и Category в Django admin.
- Настраивает отображение списков, фильтры и поля для поиска.

Каждый класс-настройка наследует от `admin.ModelAdmin` и определяет:
- list_display: поля, отображаемые в таблице списка объектов.
- list_filter: поля, доступные как фильтры в боковой панели.
- search_fields: поля, по которым выполняется полнотекстовый поиск.
"""

@admin.register(Product)
class AuthorAdmin(admin.ModelAdmin):
    """
    Конфигурация админки для модели Product.

    Атрибуты:
    - list_display (tuple): Поля, отображаемые в списке записей админки.
      Здесь отображаются идентификатор, название, цена и связанная категория.
    - list_filter (tuple): Поля, по которым можно фильтровать список.
      Позволяет фильтровать продукты по категории.
    - search_fields (tuple): Поля, по которым выполняется поиск в интерфейсе админки.
      Поиск выполняется по имени продукта и его описанию.
    """
    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')

@admin.register(Category)
class AuthorAdmin(admin.ModelAdmin):
    """
    Конфигурация админки для модели Category.

    Атрибуты:
    - list_display (tuple): Поля, отображаемые в списке категорий (id и имя).
    - list_filter (tuple): Поля для фильтрации списка категорий (по имени).
    - search_fields (tuple): Поля, по которым выполняется поиск (по имени).
    """
    list_display = ('id', 'name')
    list_filter = ('name',)
    search_fields = ('name',)
