from django import forms

class GoodsSearchForm(forms.Form):
    '''
    categoryname = forms.ChoiceField(
            initial = '',
            label = '商品名',
            required = False,
        )
    '''
    searchchar = forms.CharField(
            initial = '',
            label = '検索文字列',
            required = False,
        )
