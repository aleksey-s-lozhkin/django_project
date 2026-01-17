from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from catalog.forms import ProductForm
from catalog.models import Contact, Product


class HomeView(ListView):
    template_name = 'catalog/home.html'
    model = Product
    context_object_name = 'latest_products'
    paginate_by = 5
    ordering = ['-id']


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
    ordering = ['-created_at']


class ProductCreateView(CreateView):
    """Создание нового продукта"""

    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        messages.success(self.request, 'Продукт успешно создан!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Необходимо исправить ошибки в форме.')
        return super().form_invalid(form)


class ProductUpdateView(UpdateView):
    """Редактирование существующего продукта"""

    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        messages.success(self.request, 'Продукт успешно обновлен!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Необходимо исправить ошибки в форме.')
        return super().form_invalid(form)


class ProductDeleteView(DeleteView):
    """Удаление продукта"""

    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Продукт успешно удален!')
        return super().delete(request, *args, **kwargs)


class ProductDetailView(DetailView):
    """Детальная информация о продукте"""

    template_name = 'catalog/product_detail.html'
    model = Product
    context_object_name = 'product'
