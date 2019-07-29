"""
内部構成
class IndexView
    def post
    def get_context_data
class ResultList
※クラス、関数の詳細な説明はそれぞれのdocstringを参照してください
"""
from django.shortcuts import redirect
from django.views import generic

from .forms import CategorySearchForm
from .forms import GoodsSearchForm
from .models import GoodsTBL


class IndexView(generic.ListView):
    """
    親クラス
    種類：ListView
    一覧表示を行うことに特化したビューのクラス
    """

    model = GoodsTBL
    template_name = 'searchapp/index.html'
    context_object_name = 'goods_search_result'
    # ↑クエリ結果を格納する変数の名前を定義している

    # ①-1 post関数を定義(?)(taguchi)
    # 入らないけど関数自体は触っているみたいな動きをする。謎が多い。
    def post(self, request):
        """
        ユーザが入力した値を取得し、
        その値を元に商品の検索を実行
        検索結果をresult.htmlに返却する。
        """

        # ②-1(taguchi)
        # フォーム値をセッションに格納（他画面で使いたい）
        # 後からユーザが入力したフォームの値を格納するためのリストを作成（リスト名：form_value）
        form_value = [
            self.request.POST.get('category_name', None),
            self.request.POST.get('search_char', None)
        ]

        # ②-2(taguchi)　
        # ②-1で作成したフォームの値を格納するリストをセッション（request.session）に受け渡す
        request.session['form_value'] = form_value
        print(request.session['form_value'])
        # generic/list.pyのget()メソッドが呼び出される　※本当にこのタイミング？もう少し上では？

        # ②-3(taguchi)
        # redirectでページを遷移する
        self.get(request)
        return redirect('searchapp:result')

    # ①-2(taguchi)
    # get_context_dataメソッドでcontextデータをテンプレートに渡すことが出来る
    def get_context_data(self, *, object_list=None, **kwargs):
        """
         フォームの初期値に空白を設定したテンプレートを返すメソッド
         ⇒最初にサイトを呼び出すときに必ず呼ばれる
        """
        # ①-3(taguchi)
        # 親クラスのメソッド呼び出し、変数contextに格納
        # context＝テンプレートに使用できる文字列タグの存在を定義　※辞書型しか格納できない
        context = super().get_context_data(**kwargs)

        # ①-4(taguchi)
        # category_name、search_charにそれぞれ空白の文字列を設定する
        category_name = ''
        search_char = ''

        # ①-5(taguchi)
        # 初期値を格納するための辞書型を作成、変数名は「default_data」
        # ①-4で設定した中身が空白文字列の変数を辞書の中に格納。
        default_data = {'category_name': category_name,
                        'search_char': search_char}

        # ①-6(taguchi)
        # 予めインポートしてあるフォームに初期値の空白を設定して、更にフォームを変数に格納する。
        # （文字列検索フォーム＝search_form）
        # （カテゴリ検索フォーム=category_form）
        search_form = GoodsSearchForm(initial=default_data)
        category_form = CategorySearchForm(initial=default_data)

        # 入力フォームに空白を指定したテンプレートを呼び出し、返却する処理

        # ①-7(taguchi)
        # ①-3で設定したcontextに①-6でフォームをつっこんだ変数を格納して
        # フォームの入っているリスト'search_value'をテンプレートに返す。
        # ※contextって辞書型じゃないといけないと思うんだけどなんでこれでいいのかはわからない…。
        context['search_value'] = [category_form, search_form]
        return context


class ResultList(generic.ListView):
    """
    結果画面を表示する為に作成したダミークラス
    特に何の処理もしていない（テンプレートを指定しているくらい？）
    """
    model = GoodsTBL
    template_name = 'searchapp/result.html'
