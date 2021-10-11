from django.test import TestCase
from django.urls import reverse, resolve
from apps.products import views


class TestUrls(TestCase):

    def test_search_products_url_resolve(self):
        url = reverse('products')
        self.assertEquals(resolve(url).func.view_class, views.Products)

    def test_view_favorites_resolve(self):
        url = reverse('favorites')
        self.assertEquals(resolve(url).func.view_class, views.Favorites)

    def test_product_detail_view_resolve(self):
        url = reverse('details', kwargs={'product_code': 3257983526219})
        self.assertEquals(resolve(url).func.view_class, views.Details)
