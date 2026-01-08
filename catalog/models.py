from django.db import models
"""
Модели приложения каталога.

Содержит три модели:
- Category: категория товаров с названием и описанием.
- Product: продукт с названием, описанием, изображением, ссылкой на категорию,
  ценой и временными метками создания/обновления.
- Contact: контактные данные компании.
"""


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='products/%Y/%m/', verbose_name='Изображение', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name']


class Contact(models.Model):
    """
    Модель для хранения контактных данных компании.
    """
    country = models.CharField(max_length=100, verbose_name='Страна', default='Cuba')
    inn = models.CharField(max_length=20, verbose_name='ИНН', default='91-1144442')
    address = models.TextField(verbose_name='Адрес', default='Matanzas, Varadero')
    phone = models.CharField(max_length=20, verbose_name='Телефон', blank=True)
    email = models.EmailField(verbose_name='Email', blank=True)
    schedule = models.TextField(verbose_name='График работы', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f'Контакты ({self.country})'

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'