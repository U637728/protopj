from django.test.utils import override_settings

# テストクラスに継承させるTestCaseをインポート
from django.test import TestCase

# クライアントインポート
from django.test import client

# reverse関数のインポート（URLの逆引きに必要）
from django.urls import reverse

# searchapp直下のmodelsをインポート
from searchapp import models
from searchapp.models import GoodsTBL
from searchapp.models import CategoryTBL

# ViewのIndexViewをインポート（factory_categoryとfactory_ticket関数が定義されている）
from searchapp.views import IndexView
from unicodedata import category

#formからフリーフォームとプルダウンをインポート
from searchapp.forms import CategorySearchForm
from searchapp.forms import GoodsSearchForm

#HttpRequestobjectをインポート
from django.http import HttpRequest

#Requestオブジェクトの作成
from django.test.client import RequestFactory
from django.template.context_processors import request
from django.http.response import HttpResponseRedirect

"""
UnitTestの書き方
・アプリケーションの下に test から始まるファイルを作る
・django.test.TestCaseを継承したクラスを作る
・メソッド名をtestから始める


メソッド                 確認事項
assertEqual(a, b)        a == b
assertNotEqual(a, b)     a != b
assertTrue(x)            bool(x) is True
assertFalse(x)           bool(x) is False

例外が発生したらOK
def test_exception2(self):
self.assertRaises(Exception, func)

"""

# IndexViewがredirectで次のビューに遷移していることを確認するテスト
class IndexViewTest(TestCase):
    @override_settings(DEBUG=True) #テスト実行時にデバッグ=Trueで実行


    def test_post(self):
        # チェック用

        '''
        request = HttpResponseRedirect
        request.form_value = { 'category_name':'ブラウス', 'search_char':'テスト'}
        hpv = ('searchapp:index')
        response = hpv.client.get(request)
        response.client = client()
        print (response.session['form_value'])

        session = self.client.session
        session['form_value'] = ['','']
        session.save()
        '''

        response = self.client.post(reverse('searchapp:index'))
        self.assertEqual(response.status_code,302)
        '''
        # 結果が正常に返ってきていることを確認
        # 別のサイトURLにリダイレクトさせる際のresponse.status_codeのステータス…302
        response = self.client.get(response.url)
        self.assertEqual(response.status_code,200)
        print(response)
        #検索結果の値突合
        self.assertEqual(response.session['form_value'], check_form_value)
        '''

    def test_get_query_set(self):
        """カテゴリプルダウンとDBのテスト"""
        # レスポンスオブジェクト作成
        response = self.client.get(reverse('searchapp:index'))

        # 結果が正常に返ってきていることを確認
        assert response.status_code == 200