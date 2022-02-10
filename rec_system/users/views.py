from django.shortcuts import render, redirect

from rec_system.catalog.models import Product
from rec_system.users.models import User


def like_view(request, product_id):
    user = request.user
    user = User.objects.get(id=user.id)
    if request.method == "POST":
        product = Product.objects.get(id=product_id)
        if product not in user.liked_products:
            user.liked_products.add(product)
        return redirect('product', product_id=product_id)
    if request.method == "DELETE":
        product = Product.objects.get(id=product_id)
        if product in user.liked_products:
            user.liked_products.remove(product)
        return redirect('product', product_id=product_id)


