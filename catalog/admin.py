from django.contrib import admin

from .models import Category, Contact, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Административная конфигурация для модели Product (Продукт).

    Настройки:
    - list_display: поля, отображаемые в списке продуктов
    - list_filter: фильтры для быстрой навигации по продуктам
    - search_fields: поля для полнотекстового поиска
    """

    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Административная конфигурация для модели Category (Категория).

    Настройки:
    - list_display: поля, отображаемые в списке категорий
    - list_filter: фильтры для категорий
    - search_fields: поля для поиска категорий
    """

    list_display = ('id', 'name')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Административная конфигурация для модели Contact (Контактные данные).

    Используется для управления контактной информацией компании в админ-панели.

    Настройки:
    - list_display: основные поля, отображаемые в списке контактов
    - list_filter: фильтр по стране для быстрой группировки
    - search_fields: поля для поиска контактной информации
    - readonly_fields: поля, доступные только для чтения
    - fieldsets: группировка полей формы редактирования на логические блоки

    Fieldsets организуют форму редактирования:
    - Основная информация (страна, ИНН, адрес)
    - Контактные данные (телефон, email, график работы)
    - Служебная информация (метки времени создания/обновления)
    """

    list_display = ('country', 'inn', 'phone', 'email', 'updated_at')
    list_filter = ('country',)
    search_fields = ('country', 'inn', 'phone', 'email')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (
            'Основная информация',
            {'fields': ('country', 'inn', 'address'), 'description': 'Основные реквизиты компании'},
        ),
        (
            'Контактные данные',
            {'fields': ('phone', 'email', 'schedule'), 'description': 'Способы связи и график работы'},
        ),
        (
            'Служебная информация',
            {
                'fields': ('created_at', 'updated_at'),
                'classes': ('collapse',),
                'description': 'Автоматически заполняемые системные поля',
            },
        ),
    )
