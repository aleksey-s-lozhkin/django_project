from django.core.cache import cache
from django.db.models import QuerySet

from config.settings import CACHE_ENABLE
from .models import Product, Category


def get_product_from_cache():
    """
    Получает список всех продуктов из кэша или из базы данных.

    Returns:
        QuerySet: QuerySet с продуктами
    """
    if not CACHE_ENABLE:
        products = Product.objects.all()
        products.from_cache = False  # Добавляем атрибут
        return products

    key = 'product_list'

    products = cache.get(key)
    if products is not None:
        products.from_cache = True  # Добавляем атрибут
        return products

    products = Product.objects.all()
    products.from_cache = False  # Добавляем атрибут
    cache.set(key, products, timeout=3600)

    return products


def get_products_by_category(category_id: int) -> QuerySet:
    """
    Возвращает все продукты в указанной категории с учетом прав доступа.
    """
    # Базовый queryset с фильтром по категории
    products = Product.objects.filter(category_id=category_id)

    return products


def get_products_by_category_cached(category_id: int, user=None) -> tuple[QuerySet, bool]:
    """
    Возвращает кэшированный список продуктов в категории.
    """
    if not CACHE_ENABLE:
        products = get_products_by_category(category_id)
        return products, False

    # Ключ кэша для конкретной категории
    cache_key = f'category_products_{category_id}'

    # Пытаемся получить из кэша
    products = cache.get(cache_key)
    if products is not None:
        return products, True

    # Загружаем из БД
    products = get_products_by_category(category_id)

    # Сохраняем в кэш
    cache.set(cache_key, products, timeout=60*15)  # 15 минут

    return products, False


def get_category_by_id(category_id: int) -> Category:
    """Возвращает категорию по ID."""
    return Category.objects.get(id=category_id)
