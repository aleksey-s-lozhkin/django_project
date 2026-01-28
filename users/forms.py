from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        required=True,
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        required=True,
        label='Фамилия',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        required=False,
        label='Телефон',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    country = forms.CharField(
        required=False,
        label='Страна',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'country', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Пользователь с таким email уже существует')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']  # Устанавливаем email как username для совместимости

        # Устанавливаем дополнительные поля
        if 'first_name' in self.cleaned_data:
            user.first_name = self.cleaned_data['first_name']
        if 'last_name' in self.cleaned_data:
            user.last_name = self.cleaned_data['last_name']
        if 'phone' in self.cleaned_data:
            user.phone = self.cleaned_data['phone']
        if 'country' in self.cleaned_data:
            user.country = self.cleaned_data['country']

        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        fields = ('username', 'password')
