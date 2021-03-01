from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def index(request):
    message = "Hello"
    template = loader.get_template("products/index.html")
    # return HttpResponse(message)
    return HttpResponse(template.render(request=request))
