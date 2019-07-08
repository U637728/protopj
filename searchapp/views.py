from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from .models import CategoryTBL

# Create your views here.
#class test_View(TemplateView):

def Index(request):
    return render(request,'searchapp/index.html')
'''
def get_queryset(self):
    queryset = CategoryTBL.objects.values('categoryname')
    print(queryset)
'''