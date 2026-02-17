from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View

from catalog.forms import ProductForm, ModeratorProductForm
from catalog.models import Contact, Product


class HomeView(ListView):
    template_name = 'catalog/home.html'
    model = Product
    context_object_name = 'latest_products'
    paginate_by = 5

    def get_queryset(self):
        """Показываем только опубликованные продукты на главной"""
        return Product.objects.filter(is_published=True).order_by('-id')


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact'] = Contact.objects.first()
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()
        if not all([name, phone, message]):
            messages.error(request, 'Пожалуйста, заполните все поля формы.')
        else:
            messages.success(request, 'Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')
        return redirect('/contacts/')


class ProductListView(ListView):
    """Список всех продуктов"""

    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        """Разные наборы продуктов для разных пользователей"""
        queryset = Product.objects.all()

        # Анонимные пользователи видят только опубликованные
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_published=True)
        # Модераторы видят все
        elif self.request.user.groups.filter(name='moderator').exists():
            pass  # Модераторы видят все продукты
        else:
            # Обычные пользователи видят только опубликованные и свои продукты
            queryset = queryset.filter(
                is_published=True
            ) | queryset.filter(
                author=self.request.user
            )

        return queryset.order_by('-created_at')


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание нового продукта"""

    model = Product
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = reverse_lazy('users:login')

    def get_form_class(self):
        """Выбираем форму в зависимости от прав пользователя"""
        if self.request.user.groups.filter(name='moderator').exists():
            return ModeratorProductForm
        return ProductForm

    def form_valid(self, form):
        # Сохраняем автора продукта
        product = form.save(commit=False)
        product.author = self.request.user
        product.save()
        messages.success(self.request, 'Продукт успешно создан!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Необходимо исправить ошибки в форме.')
        return super().form_invalid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование существующего продукта"""

    model = Product
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = reverse_lazy('users:login')

    def get_form_class(self):
        """Выбираем форму в зависимости от прав пользователя"""
        if self.request.user.groups.filter(name='moderator').exists():
            return ModeratorProductForm
        return ProductForm

    def test_func(self):
        """Проверяем права на редактирование"""
        product = self.get_object()
        user = self.request.user

        # Модераторы могут редактировать все
        if user.groups.filter(name='Модераторы').exists():
            return True

        # Авторы могут редактировать свои продукты
        return product.author == user

    def handle_no_permission(self):
        """Обработка отказа в доступе"""
        messages.error(self.request, 'У вас нет прав для редактирования этого продукта.')
        return redirect(reverse_lazy('catalog:product_list'))

    def form_valid(self, form):
        messages.success(self.request, 'Продукт успешно обновлен!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Необходимо исправить ошибки в форме.')
        return super().form_invalid(form)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление продукта"""

    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')
    login_url = reverse_lazy('users:login')

    def test_func(self):
        """Проверяем права на удаление"""
        product = self.get_object()
        user = self.request.user

        # Модераторы могут удалять все
        if user.groups.filter(name='moderator').exists():
            return True

        # Авторы могут удалять свои продукты
        return product.author == user

    def handle_no_permission(self):
        """Обработка отказа в доступе"""
        messages.error(self.request, 'У вас нет прав для удаления этого продукта.')
        return redirect(reverse_lazy('catalog:product_list'))

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Продукт успешно удален!')
        return super().delete(request, *args, **kwargs)


class ProductDetailView(DetailView):
    """Детальная информация о продукте"""

    template_name = 'catalog/product_detail.html'
    model = Product
    context_object_name = 'product'

    def get_queryset(self):
        """Ограничиваем доступ к неопубликованным продуктам"""
        queryset = Product.objects.all()

        # Анонимные пользователи видят только опубликованные
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_published=True)
        # Модераторы видят все
        elif self.request.user.groups.filter(name='moderator').exists():
            pass  # Модераторы видят все продукты
        else:
            # Обычные пользователи видят опубликованные или свои продукты
            queryset = queryset.filter(
                is_published=True
            ) | queryset.filter(
                author=self.request.user
            )

        return queryset

    def get_context_data(self, **kwargs):
        """Добавляем информацию о правах пользователя в контекст"""
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        user = self.request.user

        # Проверяем, является ли пользователь модератором
        is_moderator = user.groups.filter(name='moderator').exists()

        # Права на редактирование/удаление
        can_edit = user.is_authenticated and (is_moderator or product.author == user)

        context['can_edit'] = can_edit
        context['can_delete'] = can_edit
        context['is_moderator'] = is_moderator

        return context


# Дополнительные представления для модераторов
class ModeratorRequiredMixin(UserPassesTestMixin):
    """Миксин для проверки прав модератора"""

    def test_func(self):
        return self.request.user.groups.filter(name='moderator').exists()

    def handle_no_permission(self):
        messages.error(self.request, 'Доступ только для модераторов.')
        return redirect(reverse_lazy('catalog:home'))


class ProductPublishView(ModeratorRequiredMixin, View):
    """Публикация продукта модератором"""

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = True
        product.save()
        messages.success(request, f'Продукт "{product.name}" опубликован!')
        return redirect('catalog:product_detail', pk=pk)


class ProductUnpublishView(ModeratorRequiredMixin, View):
    """Снятие с публикации продукта модератором"""

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save()
        messages.success(request, f'Продукт "{product.name}" снят с публикации!')
        return redirect('catalog:product_detail', pk=pk)


class ProductModerationListView(ModeratorRequiredMixin, ListView):
    """Список продуктов для модерации"""

    model = Product
    template_name = 'catalog/product_moderation_list.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        """Показываем неопубликованные продукты или все для модерации"""
        status = self.request.GET.get('status', 'draft')

        if status == 'published':
            return Product.objects.filter(is_published=True).order_by('-created_at')
        elif status == 'draft':
            return Product.objects.filter(is_published=False).order_by('-created_at')
        else:
            return Product.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        """Добавляем статистику"""
        context = super().get_context_data(**kwargs)
        context['published_count'] = Product.objects.filter(is_published=True).count()
        context['draft_count'] = Product.objects.filter(is_published=False).count()
        context['current_status'] = self.request.GET.get('status', 'draft')
        return context
