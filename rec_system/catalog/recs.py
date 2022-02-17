from rec_system.catalog.models import Product
from rec_system.catalog.utils import common_similarity
from rec_system.users.models import User


def add_ratio_threshold(func):

    def wrapper(*args, **kwargs):
        with_ratio = kwargs.pop('with_ratio', False)
        threshold = kwargs.pop('threshold', 0.0)
        recs_list = func(*args, **kwargs)
        if threshold:
            recs_list = [rec for rec in recs_list if rec[1] > threshold]
        if with_ratio:
            return recs_list
        return [rec[0] for rec in recs_list]

    return wrapper


@add_ratio_threshold
def get_simple_recs(product: Product):
    other_products_list = list(Product.objects.exclude(id=product.id))
    recs_list = [[item, common_similarity(product, item)] for item in other_products_list]
    recs_list.sort(key=lambda t: t[1], reverse=True)
    return recs_list


@add_ratio_threshold
def get_reaction_recs(product: Product, user: User):
    liked_products = set(user.liked_products.all())
    similar_to_liked_products = set()
    for item in liked_products:
        similar_to_item = get_simple_recs(item, threshold=0.8)
        similar_to_liked_products.update(similar_to_item)

    disliked_products = set(user.disliked_products.all())
    similar_to_disliked_products = set()
    for item in disliked_products:
        similar_to_item = get_simple_recs(item, threshold=0.8)
        similar_to_disliked_products.update(similar_to_item)

    recs_list = get_simple_recs(product, with_ratio=True)
    for rec in recs_list:
        item = rec[0]
        ratio = rec[1]
        if item in liked_products:
            ratio += 0.8
        elif item in similar_to_liked_products:
            ratio += 0.2
        if item in disliked_products:
            ratio -= 0.8
        elif item in similar_to_disliked_products:
            ratio -= 0.2
        rec[1] = ratio

    max_ratio = max(recs_list, key=lambda x: x[1])[1]
    recs_list = [[rec[0], rec[1]/max_ratio] for rec in recs_list]
    recs_list.sort(key=lambda t: t[1], reverse=True)
    return recs_list


@add_ratio_threshold
def get_many_products_recs(product_list: list, data_filter=None):
    product_list_ids = [i.id for i in product_list]
    other_products = Product.objects.exclude(id__in=product_list_ids)
    if data_filter:
        other_products = other_products.filter(**data_filter)
    other_products_list = list(other_products)
    if not other_products_list:
        return []
    recs_dict = {}
    for product in product_list:
        product_recs_list = [[item, common_similarity(product, item)] for item in other_products_list]
        for item in product_recs_list:
            recs_dict[item[0].id] = item[1] if item[0].id not in recs_dict \
                else recs_dict[item[0].id] + item[1]
    
    max_value = max(recs_dict, key=lambda x:recs_dict[x])
    recs_list = [[Product.objects.get(id=key), value/max_value] for key, value in recs_dict.items()]
    recs_list.sort(key=lambda t: t[1], reverse=True)
    return recs_list


@add_ratio_threshold
def get_many_products_reaction_recs(product_list: list, user: User, data_filter=None):
    liked_products = set(user.liked_products.all())
    similar_to_liked_products = set()
    for item in liked_products:
        similar_to_item = get_simple_recs(item, threshold=0.8)
        similar_to_liked_products.update(similar_to_item)

    disliked_products = set(user.disliked_products.all())
    similar_to_disliked_products = set()
    for item in disliked_products:
        similar_to_item = get_simple_recs(item, threshold=0.8)
        similar_to_disliked_products.update(similar_to_item)

    recs_list = get_many_products_recs(product_list, data_filter=data_filter, with_ratio=True)
    for rec in recs_list:
        item = rec[0]
        ratio = rec[1]
        if item in liked_products:
            ratio += 0.8
        elif item in similar_to_liked_products:
            ratio += 0.2
        if item in disliked_products:
            ratio -= 0.8
        elif item in similar_to_disliked_products:
            ratio -= 0.2
        rec[1] = ratio
    if not recs_list:
        return []
    max_ratio = max(recs_list, key=lambda x: x[1])[1]
    recs_list = [[rec[0], rec[1]/max_ratio] for rec in recs_list]
    recs_list.sort(key=lambda t: t[1], reverse=True)
    return recs_list


def safe_pop(result_dict, key):
    try:
        return result_dict.pop(key)
    except:
        return None


def get_soft_filter_products(filter_data: dict):
    new_products = Product.objects.filter(**filter_data)
    while not new_products.exists():
        for key in filter_data:
            if str(key).count('__lte'):
                filter_data[key] = float(filter_data[key]) * 1.25
            if str(key).count('__gte'):
                filter_data[key] = float(filter_data[key]) * 0.75
            new_products = Product.objects.filter(**filter_data)
            if new_products.exists():
                return new_products
        keys_list = list(filter_data.keys())[::-1]
        filter_data.pop(keys_list[0])
        new_products = Product.objects.filter(**filter_data)
    return new_products
