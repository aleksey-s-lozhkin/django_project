from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=35, verbose_name='Phone', blank=True, null=True, help_text='Enter your phone number')
    avatar = models.ImageField(upload_to='avatar/%Y/%m', verbose_name='Avatar', blank=True, null=True)
    country = models.CharField(max_length=10, verbose_name='Country', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
