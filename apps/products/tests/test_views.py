from django.test import TestCase, Client
from django.urls import reverse
from apps.products.models import Product, Category, Favorite
from django.contrib.auth.models import User
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse('home')
        self.legals_url = reverse('legal_notices')

    def test_index(self):
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/base.html')

    def test_legals(self):
        response = self.client.get(self.legals_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/legals.html')


class TestProduct(TestCase):

    def setUp(self):
        self.client = Client()
        self.products_url = reverse('products')
        self.details_url = reverse("details", args=[123456789])
        self.fake_categories = Category.objects.bulk_create([
            Category(id=1000, name='boulangerie'),
            Category(id=1001, name='Dessert')
        ])
        self.fake_products = Product.objects.bulk_create([
            Product(
                name='pain',
                nutriscore='b',
                url='https://fr.openfoodfacts.org/produit/8410128891169/pain',
                picture='https://images.openfoodfacts.org/images/products/90444470/front_fr.64.400.jpg',
                brand='baguette',
                category_id=1000,
                code='123456789'
            ),
            Product(
                name="pain d'épices",
                nutriscore='e',
                url='https://fr.openfoodfacts.org/produit/8410128891169/pain',
                picture='https://images.openfoodfacts.org/images/products/90444470/front_fr.64.400.jpg',
                brand='baguette',
                category_id=1000,
                code='134456789'
            ),
            Product(
                name='pain de glace',
                nutriscore='b',
                url='https://fr.openfoodfacts.org/produit/8410128891169/pain',
                picture='https://images.openfoodfacts.org/images/products/90444470/front_fr.64.400.jpg',
                brand='baguette',
                category_id=1001,
                code='123457689'
            ),
            Product(
                name='flan',
                nutriscore='b',
                url='https://fr.openfoodfacts.org/produit/8410128891169/flan',
                picture='https://images.openfoodfacts.org/images/products/90444470/front_fr.64.600.jpg',
                brand='flanby',
                category_id=1001,
                code='987654321'
            ),
            Product(
                name='pain aux noix',
                nutriscore='a',
                url='https://fr.openfoodfacts.org/produit/8410128891170/pain+aux+noix',
                picture='https://images.openfoodfacts.org/images/products/90444470/front_fr.64.500.jpg',
                brand='baguette',
                category_id=1000,
                code='123456790'
            ),
            Product(
                name='glace au flan',
                nutriscore='a',
                url='https://fr.openfoodfacts.org/produit/8410128891169/glace',
                picture='https://images.openfoodfacts.org/images/products/90444470/front_fr.64.700.jpg',
                brand='glacetop',
                category_id=1001,
                code='987654322'
            )
        ])

    def test_search_products(self):
        """Good template used to display products"""
        response = self.client.get(self.products_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/search.html')

    def test_search_index_user_question_get(self):
        """User input used for request"""
        response = self.client.get(
            self.products_url, {"product": "pizza"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "lait")

    def test_search_index_user_empty_question_get(self):
        """Good error message displayed for empty request"""
        response = self.client.get(
            self.products_url, {"product": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nous n'avons pas compris votre demande")

    def test_substitute_found(self):
        """Substitute displayed depends on category, nutriscore and name_contains_request"""
        response = self.client.get(
            self.products_url, {"product": "pain"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['object_list'][0].code, self.fake_products[4].code)
        self.assertEqual(len(response.context_data['object_list']), 1)

    def test_no_substitute_found(self):
        """No substitutes found and correct error message displayed"""
        response = self.client.get(
            self.products_url, {"product": "chorizo"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['object_list']), 0)
        self.assertContains(response, "Nous n'avons trouvé aucun produit de substitution pour")

    def test_details_page_for_product_GET(self):
        """web page for products details well displayed only if product code is valid"""
        response = self.client.get("/products/123456789")
        redirected_response = self.client.get("/products/123")
        response2 = self.client.get("/products/123", follow=True)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(redirected_response.status_code, 301)
        self.assertEqual(redirected_response.url, '/products/123/')
        self.assertEqual(response2.status_code, 200)
        self.assertRedirects(response, self.details_url, status_code=301)
        self.assertTemplateUsed(response2, '404.html')


class TestFavorites(TestCase):

    def setUp(self):

        self.client = Client()
        self.save_url = reverse('save_product_into_favorite')
        self.delete_url = reverse('delete_product_into_favorite')
        self.favorites_url = reverse('favorites')
        self.fake_user = User.objects.create_user(username='Francis', email='fkuck@lspd.ls', password='kuckaracha')
        self.fake_user.save()
        self.client.login(username="Francis", password="kuckaracha")
        self.fake_category = Category.objects.create(id=1001, name='fruit')
        self.fake_category.save()
        self.fake_product = Product.objects.create(
            name='Pamplemousse',
            nutriscore='a',
            url='https://fr.openfoodfacts.org/produit/8410128891170/pamplemousse',
            picture='https://images.openfoodfacts.org/images/products/90444470/front_fr.64.500.jpg',
            brand='failyV',
            category_id=1001,
            code='987654321'
        )
        self.fake_product.save()

    def test_access_favorites_user_connected(self):
        """Access to 'My Products' page if connected"""
        response = self.client.get(self.favorites_url)
        self.assertEquals(response.status_code, 200)

    def test_access_favorites_user_not_connected(self):
        """Fail to access to 'My Products' page if not connected"""
        self.client.logout()
        response = self.client.get(self.favorites_url)
        self.assertEqual(response.status_code, 302)

    def test_save_product_into_favorites_POST(self):
        """product is well added to user's favorites"""
        response = self.client.post(
            self.save_url,
            data={'product_id': self.fake_product.uid, 'save_favorite': True},
            follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertEqual(Favorite.objects.first().product_id, self.fake_product.id)

    def test_delete_product_into_favorites_POST(self):
        """product is well deleted from user's favorites"""
        self.test_save_product_into_favorites_POST()
        response = self.client.post(
            self.delete_url,
            data={'product_id': Favorite.objects.first().product_id, 'delete_favorite': True},
            follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertEqual(Favorite.objects.all().count(), 0)


class Suggestion(TestCase):

    def setUp(self):
        self.client = Client()
        self.suggestion_url = reverse('suggestion')
        self.fake_categories = Category.objects.bulk_create([
            Category(id=2000, name='fruit'),
            Category(id=2001, name='extras')
        ])
        self.fake_products = Product.objects.bulk_create([
            Product(
                name='ananas',
                nutriscore='b',
                url='https://fr.openfoodfacts.org/produit/8410128891169/pain',
                picture='https://images.openfoodfacts.org/images/products/90444470/front_fr.64.400.jpg',
                category_id=2000,
                code='123456789'
            ),
            Product(
                name="anaractorou",
                nutriscore='e',
                url='https://fr.openfoodfacts.org/produit/8410128891169/pain',
                picture='https://images.openfoodfacts.org/images/products/90444470/front_fr.64.400.jpg',
                category_id=2000,
                code='134456789'
            ),
            Product(
                name='riz noir',
                nutriscore='a',
                url='https://fr.openfoodfacts.org/produit/8410128891169/glace',
                picture='https://images.openfoodfacts.org/images/products/90444470/front_fr.64.700.jpg',
                category_id=2001,
                code='987654322'
            ),
            Product(
                name='riz cantonnais',
                nutriscore='a',
                url='https://fr.openfoodfacts.org/produit/8410128891169/glace',
                picture='https://images.openfoodfacts.org/images/products/90444470/front_fr.64.700.jpg',
                category_id=2001,
                code='987654322'
            ),
            Product(
                name='riz',
                nutriscore='a',
                url='https://fr.openfoodfacts.org/produit/8410128891169/glace',
                picture='https://images.openfoodfacts.org/images/products/90444470/front_fr.64.700.jpg',
                category_id=2001,
                code='987654322'
            )
        ])

    def test_suggestion_GET(self):
        """check that each letter added modify results list"""
        response = self.client.get(self.suggestion_url, data={"term": "ri"})
        response2 = self.client.get(self.suggestion_url, data={"term": "ana"})
        response3 = self.client.get(self.suggestion_url, data={"term": "anan"})
        self.assertEquals(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 3)
        self.assertEqual(len(json.loads(response2.content)), 2)
        self.assertEqual(len(json.loads(response3.content)), 1)

