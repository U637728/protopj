from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from .models import CategoryTBL
from django.views import generic
from django.db.models import Q



# Create your views here.
#class test_View(TemplateView):
'''
def Index(request):
    return render(request,'searchapp/index.html')

def get_queryset(self):
    queryset = CategoryTBL.objects.values('categoryname')
    print(queryset)
'''

class IndexView(generic.ListView):

    model = CategoryTBL
    template_name = 'searchapp/index.html'
    context_object_name = 'categorypulldown'

    '''
    テンプレートを返す関数
    def Index(request):
        return render(request,'searchapp/index.html')
    '''

    def get_queryset(self): # 呼び出された（オーバーライドされたメソッド）
        '''
        詳細画面に表示する商品を検索する。

        # セッションに値があるときに動作する
        # ⇒最初にページに入ったときはセッションに値がないので、下のelse文が実行される

        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            title = form_value[0]
            category = form_value[1]
            price = form_value[2]


        goodsid = 'AABBCC001S003'
        productno = goodsid[:9]
        deleteflag = 1

        ■DB検索条件(and)
        製品番号 = 'AABBCC001'
        論理削除フラグ = 1
        販売開始年月日 < 現在時間(now)
        販売終了年月日 > 現在時間(now)
        '''
        #Qオブジェクトを各変数にインスタンス化
        '''
        condition_goodsid = Q() #商品IDのQオブジェクト(含め)
        exact_goodsid = Q() # 商品IDのQオブジェクト(完全一致)
        exact_productno = Q() # 製造番号のQオブジェクト(完全一致)
        condition_salesstartdate = Q() # 販売開始年月日のQオブジェクト(含め)
        condition_salesenddate = Q() # 販売終了年月日のQオブジェクト(含め)
        exact_deleteflag = Q() #論理削除フラグのQオブジェクト(完全一致)
        '''
            # クエリを発行
        '''
        exact_goodsid = Q(goodsid__exact = str(goodsid)) # 条件：商品ID='AABBCC001S003'
        condition_goodsid = Q(goodsid__contains = str(productno)) # 条件：商品IDに'AABBCC001'が含まれている
        exact_productno = Q(productno__exact = str(productno)) # 条件：製造番号='AABBCC001'
        exact_deleteflag = Q(deleteflag__exact = deleteflag) # 条件：論理削除フラグ = 1
        '''
            # 入力フォームに値が入っているかの判定
            # 変数の長さが1以上で、null値ではない場合、クエリを発行する。
        '''
            if len(title) != 0 and title[0]:
                condition_title = Q(title__contains = title)
            if len(category) != 0 and category[0]:
                condition_category = Q(category__contains = category)
            if len(price) != 0 and price[0]:
                condition_price = Q(price__contains = price)
        '''
        #categorypulldown = CategoryTBL.values_list('categoryname', flat=True)
        categorypulldown = CategoryTBL.objects.select_related().all()
        # 定義されたクエリを発行し、データをgoodsdetailsへ格納する。
        print(categorypulldown)
        return categorypulldown
        '''
        kekka = GoodsTBL.objects.select_related().all()
        kekka = GoodsTBL.objects.select_related().filter(exact_productno & exact_deleteflag)
        kekka = GoodsTBL.objects.select_related().filter(condition_goodsid & exact_deleteflag)
        kekka = GoodsTBL.objects.select_related().filter(exact_productno & exact_deleteflag).values('productno').distinct()

         定義されたクエリを発行し、データをobject_listへ格納する。
         return GoodsTBL.objects.select_related().filter(condition_productno & condition_deleteflag)

        else:
            return Good.objects.none() # 何も返さない
        '''
