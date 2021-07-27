from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ('category__name',)
    list_display = ('name', 'nutriscore', 'category',)
    search_fields = ('name',)
    list_editable = ('nutriscore',)
