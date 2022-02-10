from django.contrib.auth.models import AbstractUser
from django.db import models
from rec_system.catalog.models import Product

# Create your models here.
class User(AbstractUser):
    liked_products = models.ManyToManyField(Product, related_name='users_liked', verbose_name='Понравившиеся продукты', blank=True)
    disliked_products = models.ManyToManyField(Product, related_name='users_disliked', verbose_name='Не понравившиеся продукты', blank=True)