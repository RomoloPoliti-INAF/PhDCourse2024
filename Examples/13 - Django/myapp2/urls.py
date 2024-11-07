from django.urls import path
from myapp2 import views

urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.plist, name='plist'),
    path('list/<int:id>/', views.scheda, name='scheda2'),
    path('list/add/', views.add,name="add"),
    path('list/edit/<int:id>/', views.edit,name="edit"),
    path('list/delete/<int:id>/', views.delete,name="delete"),
]
