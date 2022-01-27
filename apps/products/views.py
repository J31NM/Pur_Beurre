# pylint: disable=R0901

"""
Main Script
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView
from django.http import HttpResponseRedirect, JsonResponse
from .models import Product, Favorite


def index(request):
    """ view to main Home page """
    return render(request, 'products/index.html', {})


def legals(request):
    """ view to Legal_Notices page """
    return render(request, 'products/legals.html', {})


def error_404(request, exception=None):
    """ page to display if client error """
    context = {
        'status': 404,
        'exception': exception or ValueError('Debug mode error')
    }
    return render(request, '404.html', context)


def error_500(request, exception=None):
    """ page to display if internal server error """
    context = {
        'status': 500,
        'exception': exception or RuntimeError('Debug mode error')
    }
    return render(request, '500.html', context)


def save_product_into_favorite(request):
    """ Add product into favorites table if user uses "Sauvegarder" button """
    if 'save_favorite' in request.POST:
        product_id = request.POST.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            messages.error(request, "Ce produit n'existe plus")
            raise
        Favorite.objects.create(user=request.user, product_id=product_id)
        messages.success(request, "Le produit a bien été ajouté à vos favoris !")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_product_into_favorite(request):
    """ delete product from favorites table if user uses "Supprimer des favoris" button """
    if 'delete_favorite' in request.POST:
        product_id = request.POST.get('product_id')
        try:
            favorite = Favorite.objects.get(product_id=product_id)
        except Favorite.DoesNotExist:
            messages.error(request, "Ce produit n'existe plus")
            raise
        favorite.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def suggestion(request):
    """ fetch products in database for autocompletion """
    query_original = request.GET.get('term')
    queryset = Product.objects.filter(name__icontains=query_original)
    namelist = []
    namelist += [x.name for x in queryset]
    return JsonResponse(namelist[:25], safe=False)


class PaginatedListView(ListView):
    """ Set number of products displayed per pages """
    paginate_by = 12


class Products(PaginatedListView):
    """ Display products form database depending on user input  """
    model = Product
    template_name = 'products/search.html'
    _query = ''
    _selected_product = None

    def get_context_data(self, *args, **kwargs):
        """ define the product to search """
        Product.user = self.request.user
        context = super().get_context_data(*args, **kwargs)
        context['query'] = self._query
        try:
            context['product'] = self._selected_product
        except IndexError:
            pass
        return context

    def get_queryset(self):
        """ Get all the products into database that meet three criteria :
         - contain the product name
         - belong to the same category
         - have a higher nutriscore"""
        self._query = query = self.request.GET.get('product', "")
        if not query:
            return []
        products = Product.objects.filter(name__icontains=query)
        if not products:
            return []
        self._selected_product = products.first()
        return list(products.filter(category=self._selected_product.category,
                                    nutriscore__lt=self._selected_product.nutriscore))


class Details(ListView):
    """ display the selected product details page """
    model = Product
    template_name = 'products/details.html'

    def get(self, request, **options):
        """ use the product_code selected by the user to get the data into the database """
        product_code = options.get('product_code')
        pc = self.model.objects.filter(code=product_code)
        if not pc:
            return error_404(request)
        else:
            product = self.model.objects.filter(code=product_code).first()
            return render(request, self.template_name, {'product': product})


class Favorites(LoginRequiredMixin, PaginatedListView):
    """ Display products saved by the registered user """
    login_url = reverse_lazy('login')
    model = Favorite
    template_name = 'products/favorites.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        """ """
        Product.user = self.request.user
        context = super().get_context_data(*args, **kwargs)
        context['object_list'] = [favorite.product for favorite in context['object_list']]
        return context

