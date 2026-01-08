from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Загружает фикстуры и проверяет данные через ORM'

    def handle(self, *args, **options):
        # Очистка базы
        self.stdout.write("Очищаем базу...")
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Загрузка фикстур через call_command
        self.stdout.write("\nЗагружаем фикстуры...")

        try:
            call_command('loaddata', 'category_fixture.json')
            call_command('loaddata', 'product_fixture.json')
            self.stdout.write(self.style.SUCCESS("Фикстуры загружены"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка: {e}"))
            return

        # Проверяем через ORM-запросы
        self.stdout.write("\nПроверяем загруженные данные...")

        # Все категории
        categories = Category.objects.all()
        self.stdout.write(f"Категорий загружено: {categories.count()}")

        for category in categories:
            self.stdout.write(f"{category.name}: {category.description[:30]}...")

        # Все продукты
        products = Product.objects.all()
        self.stdout.write(f"\nПродуктов загружено: {products.count()}")

        for product in products[:5]:  # Показываем первые 5
            self.stdout.write(f"{product.name}: {product.price} руб. ({product.category.name})")
