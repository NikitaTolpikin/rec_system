# Generated by Django 3.2 on 2022-02-10 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20220209_1921'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='disliked_products',
            field=models.ManyToManyField(blank=True, related_name='users_disliked', to='catalog.Product', verbose_name='Не понравившиеся продукты'),
        ),
        migrations.AlterField(
            model_name='user',
            name='liked_products',
            field=models.ManyToManyField(blank=True, related_name='users_liked', to='catalog.Product', verbose_name='Понравившиеся продукты'),
        ),
    ]