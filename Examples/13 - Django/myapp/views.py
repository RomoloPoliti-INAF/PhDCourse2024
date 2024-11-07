from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Example

# Create your views here.

def index(request):
    var="Hello World"
    return HttpResponse(var)

def test(request):
    tmpl=loader.get_template('myapp/index.html')
    context={
        'title': 'My First title',
    }
    return HttpResponse(tmpl.render(context,request))

def list(request):
    tmpl=loader.get_template('myapp/list.html')
    dat=Example.objects.filter(name='pippo')
    context={
        'title': 'Data list',
        'data':dat,
    }
    return HttpResponse(tmpl.render(context,request))