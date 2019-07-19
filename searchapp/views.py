from django.db.models import Count
from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views import generic
from django.views import View
from django.views.generic.base import TemplateView

from .forms import CategorySearchField
from .forms import CategorySearchForm
from .models import CategoryTBL
from .forms import GoodsSearchForm
from .models import GoodsTBL
from django.forms import ModelChoiceField


'''
class TestView(TemplateView):
    template_name = 'searchapp/result.html'
    index=test_View.as_view()
'''


class IndexView(generic.ListView):
    """
    親クラス
    種類：ListView
    一覧表示を行うことに特化したビューのクラス
    """

    model = GoodsTBL
    template_name = 'searchapp/index.html'
    context_object_name = 'goods_search_result'
    #↑クエリ結果を格納する変数の名前を定義している

    #①-1 post関数を定義(taguchi)
    def post(self, request, *args, **kwargs):
        """
        ユーザが入力した値を取得し、
        その値を元に商品の検索を実行
        検索結果をresult.htmlに返却する。
        """


        #②-1(taguchi)
        #フォーム値をセッションに格納（他画面で使いたい）
        #後からユーザが入力したフォームの値を格納するためのリストを作成（リスト名：form_value）
        form_value = [
            self.request.POST.get('category_name',None),
            self.request.POST.get('search_char',None)
        ]


        #②-2(taguchi)　
        #②-1で作成したフォームの値を格納するリストをセッション（request.session）に受け渡す
        request.session['form_value'] = form_value
        # generic/list.pyのget()メソッドが呼び出される　※本当にこのタイミング？もう少し上では？

         #②-3(taguchi)
         #セッションの中にユーザの入力値が入っているかどうかの判定
         #↑（検索押した後に動いているので基本的にはなにかしら入ってる：Nullではない）
         #入っている場合は変数form_valueの中に②-2でユーザ入力値を格納したセッションを格納する
         #変数category_nameとsearch_charにユーザの入力値を格納する
         #↑（リストform_valueの番号を指定）

        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            category_name=form_value[0]
            search_char=form_value[1]
            #print(self.request.session['form_value'])

            #②-4(taguchi)
            #Qオブジェクトを作成。
            q_cate=Q(categoryid__exact=category_name)
            q_name=Q(goodsname__contains=search_char)
            q_color=Q(colorname__contains=search_char)
            q_price=Q(price__contains=search_char)
            q_size=Q(sizename__contains=search_char)
            q_ronsaku=Q(deleteflag__exact=0)

            #②-5(taguchi)
            #入力値（カテゴリプルダウンと入力フォーム）が空白どうかの条件分岐if文
            #分岐先で指定のクエリセットを発行し、変数goods_search_resultの中に格納する
            if (
                form_value[0:1]==['']
                ):
                if (
                    form_value[1:2]==['']):
                    #カテゴリ×文字×
                    goods_search_result = \
                    GoodsTBL.objects.select_related().filter(q_ronsaku)\
                    .order_by('-salesstartdate').values('goodsname').distinct()
                    print(goods_search_result)
                else:
                    #カテゴリ×文字〇
                    goods_search_result = \
                    GoodsTBL.objects.select_related()\
                    .filter(q_name | q_color | q_price | q_size).distinct()\
                    .order_by('-salesstartdate')
            else:
                if form_value[1:2]==['']:
                    #カテゴリ〇文字×
                    goods_search_result = \
                    GoodsTBL.objects.select_related()\
                    .filter(q_cate,q_ronsaku).values('goodsname').distinct()\
                    .order_by('-salesstartdate')
                else:
                    #カテゴリ〇文字〇
                    goods_search_result = \
                    GoodsTBL.objects.select_related()\
                    .filter( q_cate, ( q_name | q_color | q_price | q_size))\
                    .values('goodsname').distinct().order_by('-salesstartdate')
                    print(goods_search_result)
                    #②-6(taguchi)
                    #②-5で作成された検索結果goods_search_resultを
                    #searchapp/result.htmlに返却し、結果を表示する。

            return render(request, 'searchapp/result.html',
                          {'goods_search_result':goods_search_result})


    def get_context_data(self, **kwargs):#①-2(taguchi)
        """
         フォームの初期値に空白を設定したテンプレートを返すメソッド
         ⇒最初にサイトを呼び出すときに必ず呼ばれる
        """
        #①-3(taguchi)
        # 親クラスのメソッド呼び出し、変数contextに格納
        #context＝テンプレートに使用できる文字列タグの存在を定義　※辞書型しか格納できない
        context = super().get_context_data(**kwargs)

        #①-4(taguchi)
        #category\name、search_charにそれぞれ空白の文字列を設定する
        category_name = ''
        search_char = ''

        '''
        # 最初はセッションに値が無いからこのif節は呼ばれない
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            categoryname = form_value[0]
            print(form_value[1])
            categoryname = CategoryTBL.objects.select_related().all()
            searchchar = form_value[1]
        '''

        #①-5(taguchi)
        #初期値を格納するための辞書型を作成、変数名は「default_data」
        #①-4で設定した中身が空白文字列の変数を辞書の中に格納。
        default_data = {'category_name':category_name, 'search_char':search_char}

        #①-6(taguchi)
        #予めインポートしてあるフォームに初期値の空白を設定して、更にフォームを変数に格納する。
        #（文字列検索フォーム＝search_form）
        #（カテゴリ検索フォーム=category_form）
        search_form = GoodsSearchForm(initial = default_data)
        category_form =CategorySearchForm(initial = default_data)

        # 入力フォームに空白を指定したテンプレートを呼び出し、返却する処理

        #①-7(taguchi)
        #①-3で設定したcontextに①-6でフォームをつっこんだ変数を格納して
        #フォームの入っているリスト'search_value'をテンプレートに返す。
        #※contextって辞書型じゃないといけないと思うんだけどなんでこれでいいのかはわからない…。
        context['search_value'] = [category_form,search_form]
        return context
