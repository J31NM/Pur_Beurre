from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse_lazy
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


class Products(ListView):
    model = Product
    paginate_by = 6
    template_name = 'products/search.html'


class Details(ListView):
    model = Product
    template_name = 'products/details.html'

    def get(self, request, **options):
        pid = options.get('product_id')
        if not pid or not str(pid).isdigit():
            raise ValueError('Invalid Product ID provided')
        product = self.model.objects.get(id=int(pid))
        return render(request, self.template_name, {'product': product})


class Favorites(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    # redirect_field_name = 'redirect_to'
    model = Favorite
    template_name = 'products/favorites.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["object_list"] = [favorite.product for favorite in context["object_list"]]
        return context
