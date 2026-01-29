from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'country', 'avatar', 'password1', 'password2')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.com'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 123-45-67'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Россия'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы ко всем полям
        for field_name, field in self.fields.items():
            if field_name not in ['avatar']:
                field.widget.attrs.update({'class': 'form-control'})

        self.fields['email'].label = 'Email'

        self.fields['avatar'].help_text = 'JPG, PNG, GIF до 2 МБ'
        self.fields['avatar'].validators = [
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'],
                message='Разрешены только файлы: JPG, PNG, GIF, WebP',
            )
        ]

        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({'placeholder': 'Минимум 8 символов'})
            self.fields['password1'].label = 'Пароль'
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({'placeholder': 'Повторите пароль'})
            self.fields['password2'].label = 'Подтверждение пароля'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('Email обязателен')

        email = email.lower().strip()

        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Пользователь с таким email уже существует')
        return email

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # Проверка размера (2 МБ)
            max_size = 2 * 1024 * 1024
            if avatar.size > max_size:
                raise ValidationError('Максимальный размер файла: 2 МБ')
        return avatar

    def save(self, commit=True):

        self.cleaned_data['email'] = self.cleaned_data['email'].lower().strip()

        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']  # Для совместимости

        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',  # Явно указываем label
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.com'}),
    )
    password = forms.CharField(
        label='Пароль',  # Явно указываем label
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}),
    )

    class Meta:
        fields = ('username', 'password')
