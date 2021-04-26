from django.urls import path
# from . import views
from .views import Products, Favorites, Details

urlpatterns = [
    path('search_products/', Products.as_view(), name="products"),
    path('my_products/', Favorites.as_view(), name="favorites"),
    path(r'(<product_code>\w+)/', Details.as_view(), name="details"),
]

