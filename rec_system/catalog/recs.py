from rec_system.catalog.models import Product
from rec_system.catalog.utils import common_similarity
from rec_system.users.models import User


def get_simple_recs(product: Product, with_ratio=False, threshold=0.0):
    other_products_list = list(Product.objects.exclude(id=product.id))
    recs_list = [[item, common_similarity(product, item)] for item in other_products_list]
    recs_list.sort(key=lambda t: t[1], reverse=True)
    if threshold:
        recs_list = [rec for rec in recs_list if rec[1] > threshold]
    if with_ratio:
        return recs_list
    return [rec[0] for rec in recs_list]


def get_reaction_recs(product: Product, user: User, with_ratio=False, threshold=0.0):
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
            ratio *= 1.4
        elif item in similar_to_liked_products:
            ratio *= 1.2
        if item in disliked_products:
            ratio *= 0.6
        elif item in similar_to_disliked_products:
            ratio *= 0.8
        rec[1] = ratio

    max_ratio = max(recs_list, key=lambda x: x[1])[1]
    recs_list = [[rec[0], rec[1]/max_ratio] for rec in recs_list]
    recs_list.sort(key=lambda t: t[1], reverse=True)

    if threshold:
        recs_list = [rec for rec in recs_list if rec[1] > threshold]
    if with_ratio:
        return recs_list
    return [rec[0] for rec in recs_list]

