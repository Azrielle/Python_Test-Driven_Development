from .base import FunctionalTest
from .list_page import ListPage

class MyListsTest(FunctionalTest):
	'''тест ариложения "Мои списки"'''

	def test_logged_in_users_lists_are_saved_as_my_lists(self):
		'''тест: списки зарегистрированных пользователей 
		сохраняются как "мои списки"'''
		# Эдит является зарегистрированным пользователем
		self.create_pre_authenticated_session('edith@example.com')

		# Эдит открывает домашнюю страницу и начинает новый список
		self.browser.get(self.live_server_url)
		list_page = ListPage(self).add_list_item('Reticulate splines')
		list_page.add_list_item('Immanentize eschaton')
		first_list_url = self.browser.current_url

		# Она замечает ссылку на "Мои списки" в первый раз
		self.browser.find_element_by_link_text('My lists').click()

		# Она видит, что ее список находится там, и он назван
		# на основе первого элемента списка
		self.wait_for(
			lambda: self.browser.find_element_by_link_text('Reticulate splines')
		)
		self.browser.find_element_by_link_text('Reticulate splines').click()
		self.wait_for(
			lambda: self.assertEqual(self.browser.current_url, first_list_url)
		)
		
		# Она решает начать еще один список, чтобы только убедиться
		self.browser.get(self.live_server_url)
		list_page.add_list_item('Click cows')
		second_list_url = self.browser.current_url

		# Под заголовком "Мои списки" появляется новый список
		self.browser.find_element_by_link_text('My lists').click()
		self.wait_for(
			lambda: self.browser.find_element_by_link_text('Click cows')
		)
		self.browser.find_element_by_link_text('Click cows').click()
		self.wait_for(
			lambda: self.assertEqual(self.browser.current_url, second_list_url)
		)

		# Она выходит из системы. Опция "Мои списки" исчезает
		self.browser.find_element_by_link_text('Log out').click()
		self.wait_for( lambda: self.assertEqual(
			self.browser.find_elements_by_link_text('My lists'),
			[]
		))
