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
from django.conf.urls import url
from django.views.static import serve
from django.contrib import admin
from django.urls import path, include

from apps.products import views

from django.conf.urls.static import static

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('', views.index, name="home"),
    path('products/', include('apps.products.urls')),
    path('tatou/', admin.site.urls),
    path('members/', include('apps.members.urls')),
    path('legals/', views.legals, name="legal_notices"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        path('error_404/', views.error_404),
        path('error_500/', views.error_500),

    ] + urlpatterns


handler404 = 'apps.products.views.error_404'
handler500 = 'apps.products.views.error_500'


