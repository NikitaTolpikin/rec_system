from rec_system.catalog.models import Product, Category
from rec_system.catalog.enums import WarrantyType


def minkowski_dist(x:list, y:list, p:float, normalize=True) -> float:
    assert len(x) == len(y)
    result = 0
    for index, element in enumerate(x):
        result += abs(element - y[index])**p
    result = result ** (1 / p)
    if normalize:
        max_minkowski_dist = len(x)**(1/p)
        result = result/max_minkowski_dist
    return result

def chebyshev_dist(x:list, y:list) -> float:
    assert len(x) == len(y)
    result = float(max([abs(element-y[index]) for index, element in enumerate(x)]))
    return result

def cosine_similarity(x:list, y:list) -> float:
    assert len(x) == len(y)
    assert any([element != 0 for element in x])
    assert any([element != 0 for element in y])
    result = 0
    mod_x = 0
    mod_y = 0
    for index, element in enumerate(x):
        result += element*y[index]
        mod_x += element**2
        mod_y += y[index]**2
    mod_x = mod_x**(1/2)
    mod_y = mod_y**(1/2)
    return result/(mod_x*mod_y)

def tree_dist(x:Product, y:Product) -> float:
    x_ancestors_list = [x.category] + list(x.category.get_ancestors(ascending=True))
    y_ancestors_list = [y.category] + list(y.category.get_ancestors(ascending=True))
    min_level = min(x.category.get_level(), y.category.get_level())
    for item in x_ancestors_list:
        if item in y_ancestors_list:
            similar_node_level = item.get_level()
            return (min_level - similar_node_level) ** 2 / (min_level ** 2)
    return 1.0

def common_similarity(x:Product, y:Product) -> float:
    max_price = max(x.price, y.price)
    x_vector = [
        float(x.price/max_price),
        float(x.is_installment),
        float(WarrantyType.get_num(x.warranty_type)/len(WarrantyType))
    ]
    print(x_vector)
    y_vector = [
        float(y.price/max_price),
        float(y.is_installment),
        float(WarrantyType.get_num(y.warranty_type)/len(WarrantyType))
    ]
    print(y_vector)
    euclid_sim = 1 - minkowski_dist(x_vector, y_vector, 2)
    tree_sim = 1 - tree_dist(x, y)
    brand_sim = float(x.brand == y.brand)
    is_available_sim = float(y.is_available)
    return tree_sim * 0.5 + is_available_sim * 0.2 + brand_sim * 0.2 + euclid_sim * 0.1

def get_correlation_matrix(x_vector_list, y_vector_list):
    pass