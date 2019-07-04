from django.urls import path
from django.conf.urls import url
from . import views

urlspatters = [
    path('', views.Indexsearch.as_view(), name='index'),
    path('', views.searchresult.as_view(), name='result'),
]
