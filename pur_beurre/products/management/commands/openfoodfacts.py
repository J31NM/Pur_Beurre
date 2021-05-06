import os
import django
import requests
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pur_beurre.settings")
django.setup()
from django.core.management.base import BaseCommand
from products.models import Product, Category


class Command(BaseCommand):
    Help = 'Build database'

    def _fetch_categories(self):
        categories = []
        Category.objects.all().delete()
        data_category = requests.get('https://fr.openfoodfacts.org/categories&json=1').json()
        for category in data_category.get('tags', {}):
            category_size = category.get('products')
            if category_size > 1000:
                category_obj = Category.objects.create(name=category['name'])
                categories.append(category_obj)
        return categories

    def _fetch_products(self):
        products = []
        root_url = "https://fr.openfoodfacts.org/categorie/{}"
        payloads_template = {
            "page": 1,
            "page_size": 5,
            "json": True,
            # "action": 'process',
        }
        categories = self._fetch_categories()
        for category in categories:
            payloads = payloads_template.copy()
            full_url = root_url.format(category.name)
            product_list = requests.get(full_url, params=payloads)
            product_list = product_list.json()
            if not product_list:
                continue
            for p in product_list['products']:
                print(p)
                try:
                    name = p.get('product_name_fr')
                    nutriscore = p.get('nutrition_grades')
                    product_url = p.get('url')
                    picture = p.get('image_front_url')
                    brand = p.get('brands')
                    code = p.get('code')
                    if not all([name, nutriscore, product_url, picture, brand, code]):
                        continue
                    product_obj = Product.objects.create(
                        name=name, nutriscore=nutriscore, url=product_url,
                        picture=picture, brand=brand, code=code, category=category
                    )
                    products.append(product_obj)
                except Exception as issue:
                    print('Issue while fetching => {}'.format(issue))
        return len(categories), len(products)

    def handle(self, *args, **options):
        c_count, p_count = self._fetch_products()
        print('Categories fetched:', c_count, 'Product(s) fetched:', p_count)


if __name__ == '__main__':
    COMMAND = Command()
    print(COMMAND._fetch_categories())
    print(COMMAND._fetch_products())
