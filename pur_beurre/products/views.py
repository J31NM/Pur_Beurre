from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import ListView, DetailView
from django.http import HttpResponse

from .models import Category, Product, Favorite


def index(request):
    # raise RuntimeError('Oh lalala')
    return render(request, 'products/index.html', {})


def error_404(request, exception=None):
    context = {
        'status': 404,
        'exception': exception or ValueError('Debug mode error')
    }
    return render(request, '404.html', context)


def error_500(request, exception=None):
    context = {
        'status': 500,
        'exception': exception or RuntimeError('Debug mode error')
    }
    return render(request, '500.html', context)


class Products(ListView):
    model = Product
    template_name = 'products/search.html'


class Favorites(ListView):
    model = Favorite
    template_name = 'products/favorites.html'


class Details(ListView):
    model = Product
    template_name = 'products/details.html'

    def get(self, request, **options):
        pid = options.get('product_id')
        if not pid or not str(pid).isdigit():
            raise ValueError('Invalid Product ID provided')
        product = self.model.objects.get(id=int(pid))
        return render(request, self.template_name, {'product': product})
