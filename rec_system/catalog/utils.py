from rec_system.catalog.models import Product, Category
from rec_system.catalog.enums import WarrantyType
import numpy as np


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
    y_vector = [
        float(y.price/max_price),
        float(y.is_installment),
        float(WarrantyType.get_num(y.warranty_type)/len(WarrantyType))
    ]
    euclid_sim = 1 - minkowski_dist(x_vector, y_vector, 2)
    tree_sim = 1 - tree_dist(x, y)
    brand_sim = float(x.brand == y.brand)
    is_available_sim = float(y.is_available)
    return tree_sim * 0.5 + is_available_sim * 0.2 + brand_sim * 0.2 + euclid_sim * 0.1


def correlation_pearson(x_vector:list, y_vector:list) -> float:
    assert len(x_vector) == len(y_vector)
    x_average = np.average(x_vector)
    y_average = np.average(y_vector)
    numerator = 0
    denominator_x = 0
    denominator_y = 0
    for index, element in enumerate(x_vector):
        numerator += (element-x_average)*(y_vector[index]-y_average)
        denominator_x += (element-x_average)**2
        denominator_y += (y_vector[index]-y_average)**2
    return numerator/((denominator_x * denominator_y)**(1/2))


def correlation_matrix(vector_list:list):
    num_params = len(vector_list[0])
    result_matrix = np.zeros([num_params, num_params])
    for i in range(0, num_params):
        for j in range(0, i):
            if i==j:
                result_matrix[i, j] = 1.0
            else:
                x_vector = [item[i] for item in vector_list]
                y_vector = [item[j] for item in vector_list]
                cor_coef = correlation_pearson(x_vector, y_vector)
                result_matrix[i, j] = cor_coef
                result_matrix[j, i] = cor_coef
        result_matrix[i, i] = 1.0
    return result_matrix


def get_correlation_matrix(products:list):
    vector_list = [
        [
            float(x.price),
            float(x.is_installment),
            float(x.is_available),
            float(WarrantyType.get_num(x.warranty_type))
        ]
        for x in products
    ]
    return correlation_matrix(vector_list)


def filter_static_noise_in_correlation_matrix(matrix, n:int):
    for i in range(0, matrix.shape[0]):
        for j in range(0, matrix.shape[1]):
            r = matrix[i, j]
            if not r == 1:
                t_real = ((r**2*(n-2))/(1-r**2))**(1/2)
                t_table = get_students_table_value(n-2)
                if t_real <= t_table:
                    matrix[i, j] = 0.0
    return matrix


def pprint_correlation(products:list):
    print('  Цена     Рассрочка     Наличие     Гарантия')
    matrix = get_correlation_matrix(products)
    matrix = filter_static_noise_in_correlation_matrix(matrix, len(products))
    print(matrix)


def get_students_table_value(n:int) -> float:
    table = [
        (1, 12.7060),
        (2, 4.3020),
        (3, 3.1820),
        (4, 2.7760),
        (5, 2.5700),
        (6, 2.4460),
        (7, 2.3646),
        (8, 2.3060),
        (9, 2.2622),
        (10, 2.2281),
        (11, 2.2010),
        (12, 2.1788),
        (13, 2.1604),
        (14, 2.1448),
        (15, 2.1314),
        (16, 2.1190),
        (17, 2.1098),
        (18, 2.1009),
        (19, 2.0930),
        (20, 2.0860),
        (21, 2.0790),
        (22, 2.0739),
        (23, 2.0687),
        (24, 2.0639),
        (25, 2.0595),
        (26, 2.0590),
        (27, 2.0518),
        (28, 2.0484),
        (29, 2.0452),
        (30, 2.0423),
        (32, 2.0360),
        (34, 2.0322),
        (36, 2.0281),
        (38, 2.0244),
        (40, 2.0211),
        (42, 2.0180),
        (44, 2.0154),
        (46, 2.0129),
        (48, 2.0106),
        (50, 2.0086),
        (55, 2.0040),
        (60, 2.0003),
        (65, 1.9970),
        (70, 1.9944),
        (80, 1.9900),
        (90, 1.9867),
        (100, 1.9840),
        (120, 1.9719),
        (150, 1.9759),
        (200, 1.9719),
        (250, 1.9695),
        (300, 1.9679),
        (400, 1.9659),
        (500, 1.9640),
    ]
    for item in table:
        if item[0] >= n:
            return item[1]
    return table[-1][1]