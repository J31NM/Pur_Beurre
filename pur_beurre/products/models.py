from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    nutriscore = models.CharField(max_length=1)
    url = models.URLField(null=True)
    picture = models.URLField(null=True, max_length=500)
    categories = models.ManyToManyField(Category, related_name='products', blank=True)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name

