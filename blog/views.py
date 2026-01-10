from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, RedirectView, UpdateView

from .models import Post


class PostListView(ListView):
    """Список всех постов"""

    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        # Показываем только опубликованные посты
        return Post.objects.filter(is_published=True).order_by('-created_at')


class PostDetailView(DetailView):
    """Детальная страница поста"""

    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        # Увеличиваем счетчик просмотров
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save(update_fields=['views'])
        return obj


class PostCreateView(CreateView):
    """Создание нового поста"""

    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        """Обработка успешной отправки формы"""
        response = super().form_valid(form)
        messages.success(self.request, "Пост успешно создан!")
        return response


class PostUpdateView(UpdateView):
    """Редактирование поста"""

    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content', 'preview', 'is_published']

    def form_valid(self, form):
        """Добавляем сообщение об успехе"""
        response = super().form_valid(form)
        messages.success(self.request, "Пост успешно обновлен!")
        return response

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(DeleteView):
    """Удаление поста"""

    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, "Пост успешно удален!")
        return response


class PostPublishView(RedirectView):
    """Опубликовать пост через RedirectView"""

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        post.is_published = True
        post.save()

        messages.success(self.request, f'Пост "{post.title}" опубликован!')
        return reverse_lazy('blog:post_detail', kwargs={'pk': kwargs['pk']})


class PostUnpublishView(RedirectView):
    """Снять пост с публикации через RedirectView"""

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        post.is_published = False
        post.save()

        messages.warning(self.request, f'Пост "{post.title}" снят с публикации.')
        return reverse_lazy('blog:post_detail', kwargs={'pk': kwargs['pk']})
