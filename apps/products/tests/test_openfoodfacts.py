from django.test import TestCase
from apps.products.management.commands import openfoodfacts
import unittest.mock as mock

from apps.products.models import Category, Product


class TestSetUp(TestCase):

    def setUp(self):
        self.command = openfoodfacts.Command()
        self.mocked_response = mock.Mock()


class TestCategories(TestSetUp):

    def mocked_categories(self):
        return {
            "tags": [
                {
                    "id": "en:plant-based-foods-and-beverages",
                    "known": 1,
                    "name": "Aliments et boissons à base de végétaux",
                    "products": 107387,
                    "url": "https://fr.openfoodfacts.org/categorie/aliments-et-boissons-a-base-de-vegetaux"
                },
                {
                    "id": "en:bacon",
                    "known": 1,
                    "name": "Bacon",
                    "products": 234,
                    "url": "https://fr.openfoodfacts.org/categorie/bacon"
                },
                {
                    "id": "en:snacks",
                    "known": 1,
                    "name": "Snacks",
                    "products": 54739,
                    "url": "https://fr.openfoodfacts.org/categorie/snacks"
                }
            ]

        }


    @mock.patch("apps.products.management.commands.openfoodfacts.requests.get")
    def test_fetch_categories(self, mocked_request):
        expected_list = ["Aliments et boissons à base de végétaux", "Snacks"]
        self.mocked_response.json.return_value = self.mocked_categories()
        mocked_request.return_value = self.mocked_response
        answer = self.command._fetch_categories()
        self.assertEquals(len(answer), 2)
        self.assertIsInstance(answer[0], Category)
        self.assertListEqual(expected_list, [c.name for c in answer])


class TestProducts(TestSetUp):

    def mocked_products(self):
        return {
            "products": [
                {
                    "brands": "Schweppes",
                    "code": "3124480183927",
                    "image_front_url": "https://static.openfoodfacts.org/images/products/312/448/018/3927/front_fr.43.400.jpg",
                    "nutrition_grades": "d",
                    "product_name_fr": "Schweppes lemon",
                    "url": "https://fr.openfoodfacts.org/produit/3124480183927/schweppes-lemon"
                },
                {
                    "brands": "Lay's",
                    "code": "3168930009993",
                    "image_front_url": "https://static.openfoodfacts.org/images/products/316/893/000/9993/front_fr.24.400.jpg",
                    "nutrition_grades": "c",
                    "product_name_fr": "Chips",
                    "url": "https://fr.openfoodfacts.org/produit/3168930009993/chips-lay-s"
                },
                {
                    "brands": "Ferme d'Anchin",
                    "code": "3490211000260",
                    "image_front_url": "https://static.openfoodfacts.org/images/products/349/021/100/0260/front_fr.4.400.jpg",
                    "nutrition_grades": "b",
                    "product_name_fr": "Gaspacho bio",
                    "url": "https://fr.openfoodfacts.org/produit/3490211000260/gaspacho-bio-ferme-d-anchin"
                },
                {
                    "brands": "Ferme d'Anchin",
                    "code": "3490211000260",
                    "image_front_url": "https://static.openfoodfacts.org/images/products/349/021/100/0260/front_fr.4.400.jpg",
                    "nutrition_grades": "b",
                    "url": "https://fr.openfoodfacts.org/produit/3490211000260/gaspacho-bio-ferme-d-anchin"
                },
            ]
        }

    @mock.patch("apps.products.management.commands.openfoodfacts.requests.get")
    @mock.patch("apps.products.management.commands.openfoodfacts.Command._fetch_categories")
    def test_fetch_products(self, mocked_fetch_categories, mocked_request):
        category = Category(name='Aliments et boissons à base de végétaux')
        category.save()
        mocked_fetch_categories.return_value = [category]
        mocked_products = self.mocked_products()
        self.assertEqual(len(mocked_products['products']), 4)
        self.mocked_response.json.return_value = mocked_products
        mocked_request.return_value = self.mocked_response
        categories_count, products_count = self.command._fetch_products()
        products = Product.objects.all()
        self.assertEquals(categories_count, 1)
        self.assertEquals(products_count, 3)
        self.assertEquals(products.count(), 3)

