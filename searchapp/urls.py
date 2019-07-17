from . import views

from django.urls import path
from django.conf.urls import url


app_name = 'searchapp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
#    path('result/', views.TestView.as_view(), name='result'),
    #path('', views.Index, name='index'),
]

