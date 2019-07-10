from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from .models import CategoryTBL
from django.views import generic
from django.db.models import Q
from .forms import GoodsSearchForm


# Create your views here.
#class test_View(TemplateView):

class IndexView(generic.ListView):

    model = CategoryTBL
    template_name = 'searchapp/index.html'
    context_object_name = 'categorypulldown' #クエリ結果を格納する変数の名前を定義している

    def get_queryset(self): # 呼び出された（オーバーライドされたメソッド）

        #categorypulldown = CategoryTBL.values_list('categoryname', flat=True) カラム指定で取ってこれるらしいがエラー
        categorypulldown = CategoryTBL.objects.select_related().all()
        # 定義されたクエリを発行し、データを変数「categorypulldown」へ格納する。
        return categorypulldown

    '''
    def form_test(request):
        if  'button_1' in request.GET:
            form = GoodsSearchForm(request.GET)
            if form.is_valid():
                d = form.cleaned_data['searchchar']
    '''

    def post(self, request, *args, **kwargs):
        #フォーム値をセッションに格納（他画面で使いたい）

        #後からフォームの値を入れるためのリストを作成（リスト名：form_value）
        #if 'button' in self.request.POST:
        form_value = [
            #self.request.POST.get('categoryname',None),
            self.request.POST.get('searchchar',None)
        ]

        # 検索値を格納するリストをセッションで管理する
        request.session['form_value'] = form_value
        print(request.session['form_value'])
        # generic/list.pyのget()メソッドが呼び出される
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
         初期値に空白を設定したテンプレートを返すメソッド
         ⇒最初にサイトを呼び出すときに必ず呼ばれる
        """
        # 親クラスのメソッド呼び出し、変数contextに格納
        #contextというテンプレートタグに使用できる変数を作成している
        context = super().get_context_data(**kwargs)

        #categoryname = ''
        searchchar = ''

        # 最初はセッションに値が無いからこのif節は呼ばれない
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            #categoryname = form_value[0]
            #categoryname = CategoryTBL.objects.select_related().all()
            searchchar = form_value[1]

        # 辞書新規作成⇒初期値ではそれぞれ「空白」が設定
        default_data = { 'searchchar' :searchchar}
        #default_data = {'categoryname' :categoryname, 'searchchar' :searchchar}

        # 入力フォームに初期値では空白を設定する処理
        search_form = GoodsSearchForm(initial = default_data)

        # 入力フォームに空白を指定したテンプレートを呼び出し、返却する処理
        context['search_value'] = search_form
        print(search_form)
        return context
