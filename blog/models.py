from django.db import models


# title, content, preview (image), creation date, publication attribute (boolean field), number of views.
class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Контент')
    preview = models.ImageField(upload_to='blog/%Y/%m/', verbose_name='Превью', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=False, verbose_name='Признак публикации')
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = ['pk']
