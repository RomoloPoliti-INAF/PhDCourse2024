from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import *
from .forms import *
from rich.pretty import pprint


# Create your views here.

def home(request):
    context={
        'title': 'My app2',
    }
    return render(request, 'myapp2/index.html',context)

def plist(request):
    dat=Example.objects.order_by('surname')
    context={
        'title': 'Data list',
        'data':dat,
    }
    return render(request, 'myapp2/list.html',context)

def scheda(request,id):
    dat=get_object_or_404(Example,id=id)
    context={
        'title': 'Scheda',
        'data':dat,
    }
    return render(request, 'myapp2/scheda.html',context)

def add(request):
    if request.method=='POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('plist'))
    else:
        form = ExampleForm()
            
    context={
        'title': 'Add data',
        'main' : 'New Entry',
        'formset': form,
        'label': 'Add',
        'action': '/myapp2/list/add/',
    }

    return render(request, 'myapp2/form.html',context)

def edit(request,id):
    if request.method == 'POST':
        form = ExampleForm(
            request.POST, instance=get_object_or_404(Example, id=id))
        if form.is_valid():
            form.save()
            return redirect(reverse('plist'))
    else:
        form = ExampleForm(instance=get_object_or_404(Example,id=id))
            
    context={
        'title': 'Modify data',
        'main': 'Modify Entry',
        'formset': form,
        'label': 'Update',
        'action': f'/myapp2/list/edit/{id}/',
    }
    # context.update(csrf(request))

    return render(request, 'myapp2/form.html',context)

def delete(request,id):
    dat=get_object_or_404(Example,id=id)
    dat.delete()
    return redirect(reverse('plist'))