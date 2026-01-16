from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Административная конфигурация для модели Post (Пост блога).

    Настройки:
    - list_display: поля, отображаемые в списке постов
    - list_filter: фильтры для быстрой навигации по постам
    - search_fields: поля для полнотекстового поиска
    """

    list_display = ('id', 'title', 'created_at', 'is_published', 'views')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
