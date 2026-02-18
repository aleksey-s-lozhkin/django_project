from django.core.cache import cache

from config.settings import CACHE_ENABLE
from .models import Product


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