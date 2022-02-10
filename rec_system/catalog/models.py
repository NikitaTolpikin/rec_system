from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.
from rec_system.catalog.enums import WarrantyType


class Category(MPTTModel):
    title = models.CharField(max_length=512, verbose_name='Название')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return self.title


class Brand(models.Model):
    title = models.CharField(max_length=512, verbose_name='Название')

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=512, verbose_name='Название')
    price = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Цена')
    is_available = models.BooleanField(verbose_name='В наличии')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_products', verbose_name='Бренд')
    warranty_type = models.CharField(max_length=64, choices=WarrantyType.choices(), verbose_name='Гарантия')
    is_installment = models.BooleanField(verbose_name='Доступно в рассрочку')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_products',
                                 verbose_name='Категория')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title