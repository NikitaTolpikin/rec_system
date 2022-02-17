from django import forms

from rec_system.catalog.enums import WarrantyType
from rec_system.catalog.models import Brand


class SearchForm(forms.Form):
    title = forms.CharField(required=False, label=False)
    _recs_title = forms.CharField(required=False, label=False)
    price__gte = forms.DecimalField(required=False, label=False)
    _recs_price__gte = forms.DecimalField(required=False, label=False)
    price__lte = forms.DecimalField(required=False, label=False)
    _recs_price__lte = forms.DecimalField(required=False, label=False)
    brand = forms.ModelChoiceField(Brand.objects.all(), required=False, label=False, empty_label="Бренд")
    _recs_brand = forms.ModelChoiceField(Brand.objects.all(), required=False, label=False, empty_label="Бренд")
    warranty_type = forms.ChoiceField(choices=[('', 'Гарантия')]+WarrantyType.choices(), required=False,label=False)
    _recs_warranty_type = forms.ChoiceField(choices=[('', 'Гарантия')] + WarrantyType.choices(), required=False, label=False)
    is_available = forms.BooleanField(required=False, label='Есть в наличии')
    _recs_is_available = forms.BooleanField(required=False, label=False)
    is_installment = forms.BooleanField(required=False, label='В рассрочку')
    _recs_is_installment = forms.BooleanField(required=False, label=False)

    last_search_type = forms.CharField(required=True, label=False)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Введите название для поиска...'
        self.fields['price__gte'].widget.attrs['placeholder'] = 'Цена от'
        self.fields['price__lte'].widget.attrs['placeholder'] = 'Цена до'

        self.fields['_recs_title'].widget.attrs['placeholder'] = 'Введите название для поиска...'
        self.fields['_recs_price__gte'].widget.attrs['placeholder'] = 'Цена от'
        self.fields['_recs_price__lte'].widget.attrs['placeholder'] = 'Цена до'

        for field_key in self.fields:
            if str(field_key).startswith('_recs_'):
                self.fields[field_key].widget.attrs['style'] = 'display: none'
                self.fields[field_key].widget.attrs['class'] = 'recs_search'
            else:
                self.fields[field_key].widget.attrs['class'] = 'products_search'
                if str(field_key).startswith('is'):
                    self.fields[field_key].widget.attrs['style'] = 'margin-left: 4px;'

        self.fields['last_search_type'].initial = 'products_search'
        self.fields['last_search_type'].widget.attrs['style'] = 'display: none'
        self.fields['last_search_type'].widget.attrs['class'] = ''
