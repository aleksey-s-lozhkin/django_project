import os

from django import forms
from django.core.exceptions import ValidationError

from catalog.models import Product


class BaseProductForm(forms.ModelForm):
    """Абстрактная базовая форма для продуктов с общей валидацией"""

    # Константы для запрещенных слов
    FORBIDDEN_WORDS = {'казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар'}

    class Meta:
        model = Product
        fields = []
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Базовые настройки полей, которые есть во всех формах
        if 'name' in self.fields:
            self.fields['name'].widget.attrs.update(
                {'class': 'form-control', 'placeholder': 'Введите название продукта'}
            )

        if 'description' in self.fields:
            self.fields['description'].widget.attrs.update(
                {'class': 'form-control', 'placeholder': 'Введите описание продукта', 'rows': 4}
            )

        if 'category' in self.fields:
            self.fields['category'].widget.attrs.update({'class': 'form-select'})

        if 'price' in self.fields:
            self.fields['price'].widget.attrs.update(
                {'class': 'form-control', 'placeholder': '0.00', 'step': '0.01', 'min': '0'}
            )

        if 'image' in self.fields:
            self.fields['image'].widget.attrs.update({'class': 'form-control'})

    def clean_name(self):
        """Валидация названия продукта"""
        if 'name' in self.cleaned_data:
            name = self.cleaned_data.get('name', '').lower()

            for forbidden_word in self.FORBIDDEN_WORDS:
                if forbidden_word in name:
                    raise ValidationError(f'Название содержит запрещенное слово: "{forbidden_word}"')

        return self.cleaned_data.get('name')

    def clean_description(self):
        """Валидация описания продукта"""
        if 'description' in self.cleaned_data:
            description = self.cleaned_data.get('description', '').lower()

            for forbidden_word in self.FORBIDDEN_WORDS:
                if forbidden_word in description:
                    raise ValidationError(f'Описание содержит запрещенное слово: "{forbidden_word}"')

        return self.cleaned_data.get('description')

    def clean_price(self):
        """Валидация цены продукта"""
        price = self.cleaned_data.get('price')

        if price is not None and price < 0:
            raise ValidationError('Цена не может быть отрицательной')

        return price

    def clean_image(self):
        """Валидация изображения"""
        image = self.cleaned_data.get('image')

        if image:
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Размер изображения не должен превышать 5 МБ')
            allowed_extensions = ['.jpg', '.jpeg', '.png']
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in allowed_extensions:
                raise ValidationError('Допустимые форматы изображений: JPG, JPEG, PNG')

        return image


class ProductForm(BaseProductForm):
    """Форма для создания и редактирования продуктов обычными пользователями"""

    class Meta(BaseProductForm.Meta):
        fields = ['name', 'description', 'image', 'category', 'price']


class ModeratorProductForm(BaseProductForm):
    """Форма для модератора с дополнительным полем статуса публикации"""

    class Meta(BaseProductForm.Meta):
        fields = BaseProductForm.Meta.fields + ['is_published']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем CSS-класс для поля is_published
        if 'is_published' in self.fields:
            self.fields['is_published'].widget.attrs.update({'class': 'form-check-input'})


class ProductCreateForm(BaseProductForm):
    """Форма только для создания продукта (без некоторых полей)"""

    class Meta(BaseProductForm.Meta):
        fields = ['name', 'description', 'category', 'price']
        # При создании можно не требовать изображение сразу


class ProductUpdateForm(BaseProductForm):
    """Форма только для обновления продукта"""

    class Meta(BaseProductForm.Meta):
        fields = ['name', 'description', 'image', 'category', 'price']


class ModeratorProductUpdateForm(BaseProductForm):
    """Форма для обновления продукта модератором"""

    class Meta(BaseProductForm.Meta):
        fields = ['name', 'description', 'image', 'category', 'price', 'is_published']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'is_published' in self.fields:
            self.fields['is_published'].widget.attrs.update({'class': 'form-check-input'})
