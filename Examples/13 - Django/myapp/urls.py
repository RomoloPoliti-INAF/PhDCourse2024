from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('list/', views.list, name='list'),
]
