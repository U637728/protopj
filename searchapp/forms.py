from . import models

from django import forms

from .models import CategoryTBL
from django.forms import ModelChoiceField


"""
class GoodsSearchForm(forms.Form):
    '''
    categoryname = forms.ModelChoiceField(
            models.CategoryTBL.objects,
            label = '商品名',
            required = False,
#            queryset = CategoryTBL.objects.all,
            to_field_name='categoryname'
        )

    searchchar = forms.CharField(
            initial = '',
            label = '検索文字列',
            required = False,
        )
"""
'''
class GoodsSearchForm(forms.ModelChoiceField):
    def label_from_instance(self,categoryname):
         return f'{CategoryTBL.categoryname}'
# product = forms.ModelChoiceField(models.Product.objects, label='商品')
'''

class CategorySearchField(forms.ModelChoiceField):
    def label_from_instance(self,CategoryTBL ):
        return f"{CategoryTBL.categoryname}"


class CategorySearchForm(forms.Form):
    category_name = CategorySearchField(
            #models.CategoryTBL.objects,
            label = '',
            required = False,
            queryset=CategoryTBL.objects.all(),
            #to_field_name='categoryname',
        )

class GoodsSearchForm(forms.Form):
    search_char = forms.CharField(
            initial = '',
            label = '',
            required = False,
        )

