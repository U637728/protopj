from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from .models import CategoryTBL
from .models import GoodsTBL
from django.views import generic
from django.db.models import Q
from .forms import GoodsSearchForm
from django.shortcuts import render_to_response
from .forms import CategorySearchField
from .forms import CategorySearchForm
from django.forms import ModelChoiceField


# Create your views here.
'''
class test_View(TemplateView):
    template_name = 'searchapp/result.html'
    index=test_View.as_view()
'''

class IndexView(generic.ListView):

    model = GoodsTBL
    template_name = 'searchapp/index.html'
    context_object_name = 'GoodsSearchResult' #クエリ結果を格納する変数の名前を定義している

    """
    def get_queryset(self): # 呼び出された（オーバーライドされたメソッド）
        #categorypulldown = CategoryTBL.values_list('categoryname', flat=True) カラム指定で取ってこれるらしいがエラー
        categorypulldown = CategoryTBL.objects.select_related().all()
        # 定義されたクエリを発行し、データを変数「categorypulldown」へ格納する。
        return categorypulldown
    """

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
            self.request.POST.get('categoryname',None),
            self.request.POST.get('searchchar',None)
        ]

        # 検索値を格納するリストをセッションで管理する
        request.session['form_value'] = form_value
        #print(form_value[1]) #変数の中にリストがある場合リストの値が取れるのか知りたかった、できるよ。
        #print(request.session['form_value']) #フォームの値が取れてるのか確認したかった！！！！！
        # generic/list.pyのget()メソッドが呼び出される

        if 'form_value' in self.request.session:
                    form_value = self.request.session['form_value']
                    categoryname = form_value[0]
                    searchchar = form_value[1]
                    print(self.request.session['form_value'])
                    #クエリ一覧
                    cate=Q(categoryid__exact=categoryname)
                    name=Q(goodsname__contains=searchchar)
                    color=Q(colorname__contains=searchchar)
                    price=Q(price__contains=searchchar)
                    size=Q(sizename__contains=searchchar)

                    #入力値（カテゴリプルダウンと入力フォーム）が空白どうかの条件分岐if文
                    if form_value[0:1]==[''] :
                        #print('かてごりなし')
                        if form_value[1:2]==['']:
                            #print('もじなし') #カテゴリなし文字なし
                            GoodsSearchResult = GoodsTBL.objects.select_related().all().values('goodsname').distinct()
                        else:
                            #print('もじあり') #カテゴリなし文字あり
                            GoodsSearchResult = GoodsTBL.objects.select_related().filter(name | color | price | size).values('goodsname').distinct()
                    else:
                        #print('かてごりあり')
                        if form_value[1:2]==['']:
                            #print('もじなし') #カテゴリあり文字なし
                            GoodsSearchResult = GoodsTBL.objects.select_related().filter(cate).values('goodsname').distinct()
                        else:
                            #print('もじあり') #カテゴリあり文字あり
                            GoodsSearchResult = GoodsTBL.objects.select_related().filter(name,cate | color,cate | price,cate | size,cate).values('goodsname').distinct()

        #return self.get(request, *args, **kwargs)
        return render(request, 'searchapp/result.html',{'GoodsSearchResult':GoodsSearchResult})

    def get_context_data(self, **kwargs):
        """
         初期値に空白を設定したテンプレートを返すメソッド
         ⇒最初にサイトを呼び出すときに必ず呼ばれる
        """
        # 親クラスのメソッド呼び出し、変数contextに格納
        #contextというテンプレートタグに使用できる変数を作成している
        context = super().get_context_data(**kwargs)

        categoryname = ''
        searchchar = ''

        # 最初はセッションに値が無いからこのif節は呼ばれない
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            categoryname = form_value[0]
            #print(form_value[1])
            #categoryname = CategoryTBL.objects.select_related().all()
            searchchar = form_value[1]

        # 辞書新規作成⇒初期値ではそれぞれ「空白」が設定
        #default_data = { 'searchchar' :searchchar}
        default_data = {'categoryname' :categoryname, 'searchchar' :searchchar}

        # 入力フォームに初期値では空白を設定する処理
        search_form = GoodsSearchForm(initial = default_data)
        category_form =CategorySearchForm(initial = default_data)
        #category_form =CategorySearchField(queryset=CategoryTBL.objects.all())

        # 入力フォームに空白を指定したテンプレートを呼び出し、返却する処理
        context['search_value'] = [category_form,search_for]
        return context

    '''
    def get_queryset(self,**kwargs):
        #contextでもやった処理をもう一度やるのは変だけどコンテキストに続けるやり方わからないので…。
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            categoryname = form_value[0]
            searchchar = form_value[1]
            print(self.request.session['form_value'])
            #入力値（カテゴリプルダウンと入力フォーム）が空白どうかの条件分岐if文
            if form_value[0:1]==[''] :
                #print('かてごりなし')
                if form_value[1:2]==['']:
                    #print('もじなし') #カテゴリなし文字なし
                    GoodsSearchResult = GoodsTBL.objects.select_related().all().values('goodsname').distinct()
                else:
                    #print('もじあり') #カテゴリなし文字あり
                    name=Q(goodsname__contains=searchchar)
                    color=Q(colorname__contains=searchchar)
                    price=Q(price__contains=searchchar)
                    size=Q(sizename__contains=searchchar)
                    GoodsSearchResult = GoodsTBL.objects.select_related().filter(name | color | price | size).values('goodsname').distinct()
            else:
                #print('かてごりあり')
                if form_value[1:2]==['']:
                    #print('もじなし') #カテゴリあり文字なし
                    cate=Q(categoryid__exact=categoryname)
                    GoodsSearchResult = GoodsTBL.objects.select_related().filter(cate).values('goodsname').distinct()
                else:
                    #print('もじあり') #カテゴリあり文字あり
                    cate=Q(categoryid__exact=categoryname)
                    name=Q(goodsname__contains=searchchar)
                    color=Q(colorname__contains=searchchar)
                    price=Q(price__contains=searchchar)
                    size=Q(sizename__contains=searchchar)
                    GoodsSearchResult = GoodsTBL.objects.select_related().filter(name,cate | color,cate | price,cate | size,cate).values('goodsname').distinct()
            #return GoodsSearchResult
            return GoodsSearchResult
            '''