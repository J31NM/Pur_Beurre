from django.urls import path
from . import views

urlpatterns = [
    path('search_products/', views.Products.as_view(), name="products"),
    path('my_products/', views.Favorites.as_view(), name="favorites"),
    path(r'<int:product_code>/', views.Details.as_view(), name="details"),
    path(r'save_product/', views.save_product_into_favorite, name="save_product_into_favorite"),
    path(r'delete_product/', views.delete_product_into_favorite, name="delete_product_into_favorite"),
]
