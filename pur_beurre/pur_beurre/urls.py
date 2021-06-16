"""pur_beurre URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500

from products import views

if settings.FAKE_STATIC_PROD:
    from helper import fake_static_for_prod as static
else:
    from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="home"),
    path('products/', include('products.urls')),
    path('tatou/', admin.site.urls),
    # path('members/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls')),
    path('legals/', views.legals, name="legal_notices"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        path('error_404/', views.error_404),
        path('error_500/', views.error_500),

    ] + urlpatterns


handler404 = 'products.views.error_404'
handler500 = 'products.views.error_500'


