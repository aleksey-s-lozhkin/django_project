from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomAuthenticationForm, UserRegistrationForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def get_form_kwargs(self):
        """Передаем request.FILES в форму для загрузки аватарки"""
        kwargs = super().get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({'data': self.request.POST, 'files': self.request.FILES})
        return kwargs

    def form_valid(self, form):
        user = form.save()
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать!'
        message = 'Спасибо за регистрацию в нашем сервисе!'
        from_email = 'python-project-login@yandex.by'
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('catalog:home')
    form_class = CustomAuthenticationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if self.request.method == 'POST':
            data = kwargs.get('data', {}).copy()
            # Если есть поле 'email', используем его как 'username'
            if 'email' in data:
                data['username'] = data['email']

            if 'username' in data:
                data['username'] = data['username'].lower().strip()

            kwargs['data'] = data

        return kwargs


def logout_view(request):
    logout(request)
    return redirect('users:login')
