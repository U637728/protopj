from django import forms
from . import models

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
        )

    searchchar = forms.CharField(
            initial = '',
            label = '検索文字列',
            required = False,
        )

# product = forms.ModelChoiceField(models.Product.objects, label='商品')