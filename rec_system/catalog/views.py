from collections import OrderedDict

from django.http import HttpResponse
from django.shortcuts import render

from rec_system.catalog.forms import SearchForm
from rec_system.catalog.models import Category, Product
from rec_system.catalog.recs import get_simple_recs, get_reaction_recs, get_soft_filter_products, \
    get_many_products_recs, get_many_products_reaction_recs
from rec_system.users.models import User


def search_view(request):
    user = request.user
    if request.method == "POST":
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            data = search_form.cleaned_data
            _ = data.pop('last_search_type')
            data = {key: value for key, value in data.items() if value }

            recs_data = {key: value for key, value in data.items() if key.startswith('_recs_') }
            recs_data = {key.replace('_recs_', ''): value for key, value in recs_data.items()}
            recs_data = OrderedDict(recs_data)
            data = {key: value for key, value in data.items() if not key.startswith('_recs_') }
            data = OrderedDict(data)

            if 'title' in data:
                title = data.pop('title')
                data.update({'title__contains': title})
                data.move_to_end('title__contains', last=False)

            if 'title' in recs_data:
                title = recs_data.pop('title')
                recs_data.update({'title__contains': title})
                recs_data.move_to_end('title__contains', last=False)

            products = Product.objects.filter(**data)
            products_exists = True
            if not products.exists():
                products_exists = False
                products = get_soft_filter_products(data)

            recs_exists = False
            if user.is_anonymous:
                recs = get_many_products_recs(products, recs_data)
            else:
                recs = get_many_products_reaction_recs(products, user, recs_data)
            if recs:
                recs_exists = True
                recs = list(recs)[:6]

            return render(request, 'search.html', {
                'form': search_form,
                'products': products,
                'products_exists': products_exists,
                'recs': recs,
                'recs_exists': recs_exists
            })
    search_form = SearchForm()
    return render(request, 'search.html', {
        'form': search_form,
        'products': [],
        'products_exists': True,
        'recs': [],
        'recs_exists': True
    })

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
            recs = get_simple_recs(product, with_ratio=True)[:6]
            print([i[1] for i in recs])
            recs = [i[0] for i in recs]
        else:
            user = User.objects.get(id=user.id)
            is_liked = product in user.liked_products.all()
            is_disliked = product in user.disliked_products.all()
            recs = get_reaction_recs(product, user, with_ratio=True)[:6]
            print([i[1] for i in recs])
            recs = [i[0] for i in recs]
        return render(request, 'product.html', {
            'product': product,
            'recs': recs,
            'user': user,
            'is_liked': is_liked,
            'is_disliked': is_disliked,
        })
