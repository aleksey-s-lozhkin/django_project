from django.db import models
"""
Модели приложения каталога.

Содержит две модели:
- Category: категория товаров с названием и описанием.
- Product: продукт с названием, описанием, изображением, ссылкой на категорию,
  ценой и временными метками создания/обновления.

Docstrings поясняют назначение полей и метаданные (verbose_name, ordering и т.п.).
"""


# name, description
class Category(models.Model):
    """
    Модель категории.

    Поля:
    - name (CharField): наименование категории, максимум 150 символов.
    - description (TextField): описание категории.

    Метаданные (class Meta):
    - verbose_name (str): человекочитаемое имя модели в единственном числе.
    - verbose_name_plural (str): человекочитаемое имя модели во множественном числе.
    - ordering (list): порядок сортировки по умолчанию (здесь — по имени).

    Методы:
    - __str__: возвращает наименование категории для удобного отображения в админке и логах.
    """
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = [
            'name',
        ]


# name, description, image, category, price, created_at, updated_at
class Product(models.Model):
    """
    Модель продукта.

    Поля:
    - name (CharField): наименование продукта, максимум 150 символов.
    - description (TextField): подробное описание продукта.
    - image (ImageField): изображение продукта, сохраняется в каталог вида 'products/YYYY/MM/'.
      Поле может быть пустым (blank=True, null=True).
    - category (ForeignKey): связь с моделью Category, при удалении категории — запрет удаления продуктов
      (on_delete=models.PROTECT). related_name='products' позволяет обращаться к товарам через category.products.
    - price (DecimalField): цена покупки, максимум 10 цифр, 2 знака после запятой.
    - created_at (DateTimeField): дата и время создания записи, заполняется автоматически при создании.
    - updated_at (DateTimeField): дата и время последнего изменения, обновляется автоматически.

    Метаданные (class Meta):
    - verbose_name (str): человекочитаемое имя модели в единственном числе.
    - verbose_name_plural (str): человекочитаемое имя модели во множественном числе.
    - ordering (list): порядок сортировки по умолчанию (здесь — по имени).

    Методы:
    - __str__: возвращает наименование продукта для удобного отображения.
    """
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
        ordering = [
            'name',
        ]
