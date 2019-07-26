"""
adminページ（管理サイト）の設定を行っているファイル
"""
from django.contrib import admin
from .models import GoodsTBL
from .models import CategoryTBL
from .models import HighCategoryTBL

# Register your models here.

admin.site.register(HighCategoryTBL)
admin.site.register(CategoryTBL)
admin.site.register(GoodsTBL)
