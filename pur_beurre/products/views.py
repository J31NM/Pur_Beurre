from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, request

from .models import Category, Product, Favorite


def index(request):
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


class PaginatedListView(ListView):
    paginate_by = 6


class Products(PaginatedListView):
    model = Product
    template_name = 'products/search.html'

    def post(self, request):
        if 'save_favorite' in request.POST:
            product_id = request.POST.get('product_id')
            try:
                product = self.model.objects.get(id=product_id)
            except self.model.DoesNotExist:
                # TODO: Handle exceptions
                raise
            Favorite.objects.create(user=request.user, **product.to_dict)
        # TODO: Handle Ajax call to be more user-friendly (JSON data)
        return self.get(request)

    def get_context_data(self, *args, **kwargs):
        Product.user = self.request.user
        return super().get_context_data(*args, **kwargs)


class Details(ListView):
    model = Product
    template_name = 'products/details.html'

    def get(self, request, **options):
        product_code = options.get('product_code')
        if not product_code:
            raise ValueError('Invalid Product ID provided')
        product = self.model.objects.get(code=product_code)
        return render(request, self.template_name, {'product': product})


class Favorites(LoginRequiredMixin, PaginatedListView):
    login_url = reverse_lazy('login')
    model = Favorite
    template_name = 'products/favorites.html'

    def post(self, request):
        if 'delete_favorite' in request.POST:
            favorite_id = request.POST.get('product_id')
            try:
                # product = Product.objects.get(id=product_id)
                favorite = self.model.objects.get(id=favorite_id)
            except self.model.DoesNotExist:
            # except Product.DoesNotExist:
                # TODO: Handle exceptions
                raise
            favorite.delete()
            # product.favorite.delete()
            # TODO: Handle Ajax call to be more user-friendly (JSON data)
        return self.get(request)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)



