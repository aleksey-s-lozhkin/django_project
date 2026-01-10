from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, TemplateView

from catalog.models import Contact, Product


class HomeView(ListView):
    template_name = 'home.html'
    model = Product
    context_object_name = 'latest_products'
    paginate_by = 5
    ordering = ['-id']


class ContactsView(TemplateView):
    template_name = 'contacts.html'

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
            # Сюда нужно добавить логику (сохранение в БД, отправка e-mail...)
            messages.success(request, 'Ваше сообщение успешно отправлено! Мы свяжемся с вами в ближайшее время.')
        return redirect('/contacts/')


class ProductDetailView(DetailView):
    template_name = 'product_details.html'
    model = Product
    context_object_name = 'product'
