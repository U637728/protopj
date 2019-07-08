from django import forms
from __builtin__ import False

class CategoryForm(forms.Form):

    categoryname = forms.CharFields(
            initial = '',
            label = 'カテゴリ名',
            required = False,
            )

