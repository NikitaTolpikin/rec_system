from django.http import HttpResponse
from django.shortcuts import render
from rec_system.catalog.models import Category, Product
from rec_system.catalog.recs import get_simple_recs, get_reaction_recs
from rec_system.users.models import User


def search_view(request):
    return render(request, 'index.html')

def categories_view(request):
    if request.method == "GET":
        return render(request, 'categories.html', {'categories': Category.objects.all()})

def category_view(request, category_id):
    if request.method == "GET":
        category = Category.objects.get(id=category_id)
        products = category.category_products.all()
        return render(request, 'category.html', {'products': products, 'category': category})

def product_view(request, product_id):
    user = request.user
    if request.method == "GET":
        product = Product.objects.get(id=product_id)
        is_liked = False
        is_disliked = False
        if user.is_anonymous:
            recs = get_simple_recs(product)[:6]
        else:
            user = User.objects.get(id=user.id)
            is_liked = product in user.liked_products.all()
            is_disliked = product in user.disliked_products.all()
            recs = get_reaction_recs(product, user)[:6]
        return render(request, 'product.html', {
            'product': product,
            'recs': recs,
            'user': user,
            'is_liked': is_liked,
            'is_disliked': is_disliked,
        })
