from django import forms
from django.core.exceptions import ValidationError
from catalog.models import Product


class ProductForm(forms.ModelForm):
    """Форма для создания и редактирования продуктов с валидацией"""

    # Константы для запрещенных слов
    FORBIDDEN_WORDS = {
        'казино', 'криптовалюта', 'крипта', 'биржа',
        'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    }

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Стилизация всех полей формы
        for field_name, field in self.fields.items():
            if field_name != 'image':  # Для поля image отдельная обработка
                if isinstance(field.widget, forms.CheckboxInput):
                    field.widget.attrs.update({'class': 'form-check-input'})
                elif isinstance(field.widget, forms.Select):
                    field.widget.attrs.update({'class': 'form-select'})
                else:
                    field.widget.attrs.update({'class': 'form-control'})

            # Добавляем placeholder для полей
            if field_name == 'name':
                field.widget.attrs['placeholder'] = 'Введите название продукта'
            elif field_name == 'description':
                field.widget.attrs['placeholder'] = 'Введите описание продукта'
            elif field_name == 'price':
                field.widget.attrs['placeholder'] = '0.00'
                field.widget.attrs['step'] = '0.01'
                field.widget.attrs['min'] = '0'

    def clean_name(self):
        """Валидация названия продукта"""
        name = self.cleaned_data.get('name', '').lower()

        for forbidden_word in self.FORBIDDEN_WORDS:
            if forbidden_word in name:
                raise ValidationError(
                    f'Название содержит запрещенное слово: "{forbidden_word}"'
                )

        return self.cleaned_data['name']

    def clean_description(self):
        """Валидация описания продукта"""
        description = self.cleaned_data.get('description', '').lower()

        for forbidden_word in self.FORBIDDEN_WORDS:
            if forbidden_word in description:
                raise ValidationError(
                    f'Описание содержит запрещенное слово: "{forbidden_word}"'
                )

        return self.cleaned_data['description']

    def clean_price(self):
        """Валидация цены продукта"""
        price = self.cleaned_data.get('price')

        if price is not None and price < 0:
            raise ValidationError('Цена не может быть отрицательной')

        return price

    def clean_image(self):
        """Валидация изображения (дополнительное задание)"""
        image = self.cleaned_data.get('image')

        if image:
            # Проверка размера файла (5 МБ = 5 * 1024 * 1024 байт)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Размер изображения не должен превышать 5 МБ')

            # Проверка формата файла
            allowed_extensions = ['.jpg', '.jpeg', '.png']
            import os
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in allowed_extensions:
                raise ValidationError(
                    'Допустимые форматы изображений: JPG, JPEG, PNG'
                )

        return image
