from django import forms

from rec_system.catalog.enums import WarrantyType
from rec_system.catalog.models import Brand


class SearchForm(forms.Form):
    title = forms.CharField(required=False, label=False)
    price__gte = forms.DecimalField(required=False, label=False)
    price__lte = forms.DecimalField(required=False, label=False)
    brand = forms.ModelChoiceField(Brand.objects.all(), required=False, label=False, empty_label="Бренд")
    warranty_type = forms.ChoiceField(choices=[('', 'Гарантия')]+WarrantyType.choices(), required=False,label=False)
    is_available = forms.BooleanField(required=False, label='Есть в наличии')
    is_installment = forms.BooleanField(required=False, label='В рассрочку')

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Введите название для поиска...'
        self.fields['price__gte'].widget.attrs['placeholder'] = 'Цена от'
        self.fields['price__lte'].widget.attrs['placeholder'] = 'Цена до'
