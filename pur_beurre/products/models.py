from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    user = None
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=64)
    brand = models.CharField(max_length=200, blank=True, null=True)
    nutriscore = models.CharField(max_length=1)
    url = models.URLField(null=True)
    picture = models.URLField(null=True, max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', blank=True)

    @property
    def uid(self):
        return self.id

    @property
    def to_dict(self):
        return dict(
            url=self.url,
            code=self.code,
            name=self.name,
            brand=self.brand,
            picture=self.picture,
            category=self.category,
            nutriscore=self.nutriscore,
        )

    @property
    def is_favorite(self):
        if self.user is None:
            raise ValueError('No user set for product: {}'.format(self))

        if isinstance(self.user, User):
            return bool(Favorite.objects.filter(picture=self.picture, user=self.user))
        return False

    def __str__(self):
        return self.name


class Favorite(models.Model):
# class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="favorite")

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=64)
    brand = models.CharField(max_length=200, blank=True, null=True)
    nutriscore = models.CharField(max_length=1)
    url = models.URLField(null=True)
    picture = models.URLField(null=True, max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='favorites', blank=True)

    @property
    def uid(self):
        return self.picture

    @property
    def is_favorite(self):
        return True

    def __str__(self):
        return self.name
        # return self.product.name

