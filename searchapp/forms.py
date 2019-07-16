from django import forms
from . import models
from .models import CategoryTBL

class GoodsSearchForm(forms.Form):
    '''
    categoryname = forms.ChoiceField(
            initial = '',
            label = '商品名',
            required = False,
        )
    '''
    categoryname = forms.ModelChoiceField(
            models.CategoryTBL.objects,
            label = '商品名',
            required = False,
            #queryset = CategoryTBL.objects.values('categoryname'),
        )

    searchchar = forms.CharField(
            initial = '',
            label = '検索文字列',
            required = False,
        )

'''
class GoodsSearchForm(forms.ModelChoiceField):
    def label_from_instance(self,categoryname):
         return f'{CategoryTBL.categoryname}'
# product = forms.ModelChoiceField(models.Product.objects, label='商品')
'''