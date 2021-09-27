# pylint: disable=W0212
# pylint: disable=E1101

"""
Module to request OpenFoodFacts API to fill in the database with products

_fetch_categories get main categories
_fetch_products get products from each category selected if they gather the data we need :
    name, nutriscore, url, picture, brand, code (product unique id)

"""

import os
import json
import django
import requests

from django.core.management.base import BaseCommand

from apps.products.models import Product
from apps.products.models import Category

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pur_beurre.settings")
django.setup()


class Command(BaseCommand):
    """ Get products from Openfoodfacts API """
    Help = 'Build database'

    def _fetch_categories(self):
        categories = []
        Category.objects.all().delete()
        data_category = requests.get('https://fr.openfoodfacts.org/categories&json=1').json()
        for category in data_category.get('tags', {}):
            category_size = category.get('products')
            if category_size > 10000:
                category_obj = Category.objects.create(name=category['name'])
                categories.append(category_obj)
        return categories

    def _fetch_products(self):
        products = []
        root_url = "https://fr.openfoodfacts.org/categorie/{}"
        payloads_template = {
            "page": 1,
            "page_size": 100,
            "json": True,
        }
        levels_translations = {
            'low': 'faible',
            'moderate': 'modérée',
            'high': 'élevée',
        }
        categories = self._fetch_categories()
        for category in categories:
            payloads = payloads_template.copy()
            full_url = root_url.format(category.name)
            product_list = requests.get(full_url, params=payloads)
            product_list = product_list.json()
            if not product_list:
                continue
            for product in product_list['products']:
                try:
                    name = product.get('product_name_fr')
                    nutriscore = product.get('nutrition_grades')
                    product_url = product.get('url')
                    picture = product.get('image_front_url')
                    brand = product.get('brands')
                    code = product.get('code')
                    nutriments = product.get('nutriments') or {}
                    nutrient_levels = product.get('nutrient_levels') or {}
                    nutrients = {
                        'fat': {
                            'quantity': nutriments.get('fat_100g'),
                            'level': levels_translations.get(nutrient_levels.get('fat'))
                        },
                        'salt': {
                            'quantity': nutriments.get('salt_100g'),
                            'level': levels_translations.get(nutrient_levels.get('salt'))
                        },
                        'sugar': {
                            'quantity': nutriments.get('sugars_100g'),
                            'level': levels_translations.get(nutrient_levels.get('sugars'))
                        },
                        'saturated_fat': {
                            'quantity': nutriments.get('saturated-fat_100g'),
                            'level': levels_translations.get(nutrient_levels.get('saturated-fat'))
                        },
                    }

                    if not all([name, nutriscore, product_url, picture, brand, code]):
                        continue
                    product_obj = Product.objects.create(
                        name=name, nutriscore=nutriscore, url=product_url,
                        picture=picture, brand=brand, code=code, category=category,
                        nutrients_json=json.dumps(nutrients, indent=4)
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
