'''
アプリURLの設定を行っている。
path('', views.IndexView.as_view(), name='index'),
    …特に指定のない場合はIndexViewクラスに飛ばす
path('result/', views.ResultList.as_view(), name='result'),
    …パスの末尾にresult/を指定された場合はResultListクラスに飛ばす
'''
from django.urls import path  # path機能インポート(デフォルト)

from . import views  # searchapp(自分)からviews.pyインポート


app_name = 'searchapp'  # アプリの名前'searchapp'を設定

urlpatterns = [
    #URLに指定なしの場合、views.pyのIndexViewの処理を動かす
    path('', views.IndexView.as_view(), name='index'),
    #URLに'result/'を指定している場合、views.pyのResultListの処理を動かす
    path('result/', views.ResultList.as_view(), name='result'),
]
