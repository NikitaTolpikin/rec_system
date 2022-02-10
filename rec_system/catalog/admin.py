from django.contrib import admin
from rec_system.catalog.models import Category, Brand, Product

# Register your models here.

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)