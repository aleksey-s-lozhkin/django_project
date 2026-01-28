from django.views.generic import CreateView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect
from .forms import UserRegistrationForm, CustomAuthenticationForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Hello!'
        message = 'Thanks for registering now!'
        from_email = 'python-project-login@yandex.by'
        recipient_list = [user_email,]
        send_mail(subject, message, from_email, recipient_list)


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('catalog:home')
    form_class = CustomAuthenticationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        if 'data' in kwargs:
            data = kwargs['data'].copy()
            if 'email' in data and 'username' not in data:
                data['username'] = data['email']
            kwargs['data'] = data
        return kwargs

def logout_view(request):
    logout(request)
    return redirect('users/login.html')

