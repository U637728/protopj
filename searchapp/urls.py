'''
アプリURLの設定を行っている。
path('', views.IndexView.as_view(), name='index'),
    …特に指定のない場合はIndexViewクラスに飛ばす
path('result/', views.ResultList.as_view(), name='result'),
    …パスの末尾にresult/を指定された場合はResultListクラスに飛ばす
'''
from django.urls import path

from . import views


app_name = 'searchapp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('result/', views.ResultList.as_view(), name='result'),
]
