from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, request, HttpResponseRedirect

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


def save_product_into_favorite(request):
    if 'save_favorite' in request.POST:
        product_id = request.POST.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            # TODO: Handle exceptions
            raise
        Favorite.objects.create(user=request.user, **product.to_dict)
    # TODO: Handle Ajax call to be more user-friendly (JSON data)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_product_into_favorite(request):
    if 'delete_favorite' in request.POST:
        favorite_id = request.POST.get('product_id')
        try:
            # product = Product.objects.get(id=product_id)
            favorite = Favorite.objects.get(id=favorite_id)
        except Favorite.DoesNotExist:
            # TODO: Handle exceptions
            raise
        favorite.delete()
        # product.favorite.delete()
        # TODO: Handle Ajax call to be more user-friendly (JSON data)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class PaginatedListView(ListView):
    paginate_by = 6


class Products(PaginatedListView):
    model = Product
    template_name = 'products/search.html'

    def get_context_data(self, *args, **kwargs):
        Product.user = self.request.user
        context = super().get_context_data(*args, **kwargs)
        context['query'] = self.request.POST.get('product', "")
        try:
            context['product'] = context['object_list'].pop(0)
        except IndexError:
            pass
        return context

    def get_queryset(self):
        query = self.request.GET.get('product', "")
        products = Product.objects.filter(name__icontains=query)
        if not products:
            return []
        product = products.first()
        return [product] + list(products.filter(category=product.category, nutriscore__lt=product.nutriscore))


class Details(ListView):
    model = Product
    template_name = 'products/details.html'

    def get(self, request, **options):
        product_code = options.get('product_code')
        if not product_code:
            raise ValueError('Invalid Product ID provided')
        product = self.model.objects.filter(code=product_code).first()
        return render(request, self.template_name, {'product': product})


class Favorites(LoginRequiredMixin, PaginatedListView):
    login_url = reverse_lazy('login')
    model = Favorite
    template_name = 'products/favorites.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)



