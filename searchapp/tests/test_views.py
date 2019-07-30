from django.test.utils import override_settings

# テストクラスに継承させるTestCaseをインポート
from django.test import TestCase

# reverse関数のインポート（URLの逆引きに必要）
from django.urls import reverse

# searchapp直下のmodelsをインポート
from searchapp import models
from searchapp.models import GoodsTBL

# ViewのIndexViewをインポート（factory_categoryとfactory_ticket関数が定義されている）
from searchapp.views import IndexView
from unicodedata import category

#formからフリーフォームとプルダウンをインポート
from searchapp.forms import CategorySearchForm
from searchapp.forms import GoodsSearchForm

#HttpRequestobjectをインポート
from django.http import HttpRequest

#Requestオブジェクトの作成ができるらしい…
from django.test.client import RequestFactory

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

# Ticketというモデルのリスト作成に関するテストコードを定義するクラスを作成
class IndexViewTest(TestCase):

    @override_settings(DEBUG=True) #テスト実行時にデバッグ=Trueで実行

    def test_post(self):
        """
        # DBデータを事前に登録しておく
        GoodsTBL(title='ワンピース', category='スカート', price=100).save()

        #チェック用
        check_title, check_category, check_price = 'ワンピース', 'スカート', 100

        # リクエストを擬似的に送ってくれるHTTPクライアント（self.cliant）でレスポンスオブジェクトを生成
        response = self.client.post(reverse('searchapp:index'), {'title':'ワンピース', 'category':'スカート', 'price':100})

        # 結果が正常に返ってきていることを確認
        assert response.status_code == 200

        #検索結果が1件であることを確認
        self.assertEqual(response.context['object_list'].count(),1)

        #検索結果の値突合
        self.assertEqual(response.context['object_list'].first().title, check_title)
        self.assertEqual(response.context['object_list'].first().category, check_category)
        self.assertEqual(response.context['object_list'].first().price, check_price)
        """

    def test_post(self):
        #フォームの値が空白の場合、'(空白)'を取得する
        category_name =  ''
        search_char = ''

        #チェック用
        check_form_value = ['','']

        #リクエストオブジェクトの作成
        rf = RequestFactory()
        Request = rf.post('', form_value = [category_name,search_char])

        #取得した値の突合
        self.assertEqual(Request,check_form_value)

