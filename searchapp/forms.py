"""
内部構成
class CategorySearchField
    def label_from_instance
class CategorySearchForm
class GoodsSearchForm
"""
from django import forms

from .models import CategoryTBL


# ModelChoiceField=プルダウンの選択肢をmodels.pyから参照するフォームの種類
class CategorySearchField(forms.ModelChoiceField):
    """
    プルダウンフォームを表示するためのModelChoiceFormを継承したクラス
    label_from_instanceでプルダウンの値を上書きしている
    """
    #選択肢の表示をカスタマイズするメソッド
    def label_from_instance(self, obj=CategoryTBL):
        #  f"{}＝フォーマット文字列（{}内の文字をpythonの式として認識する）
        # obj.categoryname（カテゴリネーム）をmodelchoicefieldの値としてreturn
        return f"{obj.categoryname}"


class CategorySearchForm(forms.Form):
    """
    この中で↑のモデルを呼びだしてカテゴリプルダウンとして使用する
    """
    category_name = CategorySearchField(
        label='',
        required=False,  # 入力値の空白を許可
        queryset=CategoryTBL.objects.all(), # クエリ発行結果をプルダウンの選択肢に設定
        empty_label='カテゴリ',
    )


class GoodsSearchForm(forms.Form):
    """
    フリーワード検索のフォームを表示する為のクラス
    """

    """
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    """

    search_char = forms.CharField(
        max_length=180,
        initial='',
        label='',
        required=False,
        # プレイスホルダー（入力内容ヒント）の文字列を設定
        widget=forms.TextInput(
            attrs={
                'placeholder': 'フリーワード検索', 'class': 'class_name'
                }
        )
    )

    def __init__(self, *args, **kwargs):
        super(GoodsSearchForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            # class="form-inline＝formの要素を横並びに隙間なく配置する設定
            field.widget.attrs["class"] = "form-inline"
