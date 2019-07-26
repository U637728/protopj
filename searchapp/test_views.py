from django.test import TestCase
from .import views

class get_context_data_Test(Testcase):
    def setup(self):
        self.IndexView = views.IndexView

    def test_context_add(self):
        expected = super().get_context_data(**kwargs)
        actual =