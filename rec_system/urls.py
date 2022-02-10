from django.contrib import admin
from django.urls import path, include
from rec_system.catalog.views import categories_view, category_view, product_view, index_view
from rec_system.users.views import like_view, dislike_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    path('categories/', categories_view, name='categories'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('category/<int:category_id>/', category_view, name='category'),
    path('product/<int:product_id>/', product_view, name='product'),
    path('product/<int:product_id>/like/', like_view, name='product-like'),
    path('product/<int:product_id>/dislike/', dislike_view, name='product-dislike'),

]
