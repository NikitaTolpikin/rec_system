"""rec_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rec_system.catalog.views import categories_view, category_view, product_view, index_view
from rec_system.users.views import like_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    path('categories/', categories_view, name='categories'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('category/<int:category_id>/', category_view, name='category'),
    path('product/<int:product_id>/', product_view, name='product'),
    path('product/<int:product_id>/like/', like_view, name='product-like'),
]
