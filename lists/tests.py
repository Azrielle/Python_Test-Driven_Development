from django.urls import resolve
from django.test import TestCase
from lists.views import home_page

# Create your tests here.
class HomePageTest(TestCase):
	'''тест домашней страницы'''
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

		

# class SmokeTest(TestCase):
# 	'''Тест на токсичность'''

# 	def test_bad_maths(self):
# 		'''тест: неправильные математические расчеты'''
# 		self.assertEqual(1+1,3)
