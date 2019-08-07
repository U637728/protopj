"""
内部構成
class IndexView
    def post
    def get_context_data
class ResultList
※クラス、関数の詳細な説明はそれぞれのdocstringを参照してください

コメントの見方
①…機能①（検索画面表示）中の処理
②…機能②（セッションに検索文字列を格納する）中の処理
-1…デバッグで確認したポインタが触る順番
例）①-3　の場合
機能①を処理する際に３番目に動く処理
"""
from django.shortcuts import redirect
from django.views import generic

from .forms import CategorySearchForm
from .forms import GoodsSearchForm
from .models import GoodsTBL


class IndexView(generic.ListView):
    """
    検索画面表示、検索文字列取得のためのクラス
    """

    model = GoodsTBL
    template_name = 'searchapp/index.html'
    # クエリ結果を格納する変数の名前を定義している
    context_object_name = 'goods_search_result'

    # ①-1 post関数を定義
    def post(self, request):
        """
        変数form_valueに画面上の入力フォームからpostで取得した値を
        格納して、セッションに持たせるメソッド
        """
        # ②-1
        # フォーム値をセッションに格納（次画面で使用）
        # 後からユーザが入力したフォームの値を格納するためのリストを作成（リスト名：form_value）
        form_value = [
            self.request.POST.get('category_name', None),
            self.request.POST.get('search_char', None)
        ]
        # ②-2　
        # ②-1で作成したフォームの値を格納するリストをセッション（request.session）に受け渡す
        request.session['form_value'] = form_value
        # generic/list.pyのget()メソッドが呼び出される

        # ②-3
        # redirectでページを遷移する
        return redirect('searchapp:result')

    # ①-2
    # get_context_dataメソッドでcontextデータをテンプレートに渡すことが出来る
    def get_context_data(self, *, object_list=None, **kwargs):
        """
         初期値に空白を設定した入力フォームとプルダウンフォームを格納した変数を
         contextに持たせてindex.htmlへ返すメソッド
        """
        # ①-3
        # 親クラスのメソッド呼び出し、変数contextに格納
        # context＝テンプレートに使用できる文字列タグの存在を定義　※辞書型しか格納できない
        context = super().get_context_data(**kwargs)

        # ①-4
        # 検索フォームの初期値を設定する処理
        #category_name、search_charにそれぞれ空白の文字列を設定する
        category_name = ''
        search_char = ''

        # ①-5
        # 初期値を格納するための辞書型変数を作成、変数名は「default_data」
        # ①-4で設定した中身が空白文字列の変数を辞書の中に格納。
        default_data = {'category_name': category_name,
                        'search_char': search_char}

        # ①-6
        # 予めインポートしてあるフォームに初期値を設定して、更にフォームを変数に格納する。
        # （文字列検索フォーム＝search_form）
        # （カテゴリ検索フォーム=category_form）
        search_form = GoodsSearchForm(initial=default_data)
        category_form = CategorySearchForm(initial=default_data)
        # 入力フォームに空白を指定したテンプレートを呼び出し、返却する処理

        # ①-7
        # ①-3で設定したcontextに①-6でフォームを格納した変数を格納
        # テンプレートにフォームを表示させる処理
        #表示用フォームが格納されたリスト'search_value'をテンプレートに返す。
        context['search_value'] = [category_form, search_form]
        return context


class ResultList(generic.ListView):
    """
    結果画面を表示する為に作成したダミークラス
    特に何の処理もしていない（テンプレートを指定しているくらい？）
    """
    model = GoodsTBL
    template_name = 'searchapp/result.html'
