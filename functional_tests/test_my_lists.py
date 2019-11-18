from django.conf import settings
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session


class MyListsTest(FunctionalTest):
	'''тест ариложения "Мои списки"'''

	def create_pre_authenticated_session(self, email):
		'''создать предворительно аутентифицированный сеанс'''
		if self.staging_server:
			session_key = create_session_on_server(self.staging_server, email)
		else:
			session_key = create_pre_authenticated_session(email)

		## установить cookie, которые нужны для первого посещения домена.
		## страницы 404 загружаются быстрее всего!
		self.browser.get(self.live_server_url + "/404_no_such_url/")
		self.browser.add_cookie(dict(
			name=settings.SESSION_COOKIE_NAME,
			value=session_key,
			path='/'
		))

	def test_logged_in_users_lists_are_saved_as_my_lists(self):
		'''тест: списки зарегистрированных пользователей 
		сохраняются как "мои списки"'''
		# Эдит является зарегистрированным пользователем
		self.create_pre_authenticated_session('edith@example.com')

		# Эдит открывает домашнюю страницу и начинает новый список
		self.browser.get(self.live_server_url)
		self.add_list_item('Reticulate splines')
		self.add_list_item('Immanentize eschaton')
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
		self.add_list_item('Click cows')
		secpnd_list_url = self.browser.current_url

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
			self.browser.find_element_by_link_text('My lists'),
			[]
		))
