from rec_system.catalog.models import Product
from rec_system.catalog.utils import common_similarity


def get_simple_recs(product: Product):
    other_products_list = list(Product.objects.exclude(id=product.id))
    recs_list = [(item, common_similarity(product, item)) for item in other_products_list]
    recs_list.sort(key=lambda t: t[1], reverse=True)
    return recs_list

