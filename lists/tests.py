from django.test import TestCase

# Create your tests here.
class HomePageTest(TestCase):
	'''тест домашней страницы'''


	def test_home_page_returns_correct_html(self):
		'''тест: домашняя страница возвращает правильный html'''
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')

	def test_can_save_a_POST_request(self):
		response = self.client.post('/', data={'item_text': 'A new list item'})
		self.assertIn('A new list item', response.content.decode())
		self.assertTemplateUsed(response, 'home.html')