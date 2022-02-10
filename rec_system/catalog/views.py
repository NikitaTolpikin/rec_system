from django.http import HttpResponse
from django.shortcuts import render
from rec_system.catalog.models import Category, Product
from rec_system.catalog.recs import get_simple_recs, get_reaction_recs


def index_view(request):
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
        if user.is_anonymous:
            recs = get_simple_recs(product)
        else:
            recs = get_reaction_recs(product, user)
        return render(request, 'product.html', {'product': product, 'recs': recs, 'user': user})
