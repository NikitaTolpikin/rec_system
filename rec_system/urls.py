from django.contrib import admin
from django.urls import path, include
from rec_system.catalog.views import categories_view, category_view, product_view, search_view
from rec_system.users.views import like_view, dislike_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', search_view, name='search'),
    path('categories/', categories_view, name='categories'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('category/<int:category_id>/', category_view, name='category'),
    path('product/<int:product_id>/', product_view, name='product'),
    path('product/<int:product_id>/like/', like_view, name='product-like'),
    path('product/<int:product_id>/dislike/', dislike_view, name='product-dislike'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
