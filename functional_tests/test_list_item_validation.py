from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
	'''тест валидации элемента списка'''
	def get_error_element(self):
		'''получить элемент с ошибкой'''
		return self.browser.find_element_by_css_selector('.has-error')

	def test_cannot_add_empty_list_item(self):
		'''тест: нельзя добавить пустой элемент списка'''
		# Эдит открывает домашнюю страницу и случайно пытается отправить
		# пустой элемент списка. Она надимает Enter на пустом поле ввода
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys(Keys.ENTER)

		# Браузер перехватывает запрос и не загружает страницу со списком
		self.wait_for(lambda: self.browser.find_element_by_css_selector(
			'#id_text:invalid'
		))
		# Эдин начинает набирать текст нового элемента и ошибка исчезает
		self.get_item_input_box().send_keys('Buy milk')
		self.wait_for(lambda: self.browser.find_element_by_css_selector(
			'#id_text:valid'
		))

		# И она может отправить его успешно
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		# Как ни странно, Эдит решает отправить второй пустой элемент списка
		self.get_item_input_box().send_keys(Keys.ENTER)

		# И снова браузер неподчиняется
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for(lambda: self.browser.find_element_by_css_selector(
			'#id_text:invalid'
		))
		# И она может его исправить, заполнив поле неким текстом
		self.get_item_input_box().send_keys('Make tea')
		self.wait_for(lambda: self.browser.find_element_by_css_selector(
			'#id_text:valid'
		))

		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for_row_in_list_table('2: Make tea')

	def test_cannot_add_duplicate_items(self):
		'''тест: нельзя добовлять повторяющиеся элементы'''
		# Эдит открывает домашнюю страницу и начинает новый список
		self.browser.get(self.live_server_url)
		self.add_list_item('Buy wellies')

		# Она случайно пытается ввести повторяющийся элемент
		self.get_item_input_box().send_keys('Buy wellies')
		self.get_item_input_box().send_keys(Keys.ENTER)

		# Она видит полезное сообщение об ошибке
		self.wait_for(lambda: self.assertEqual(
			self.get_error_element().text,
			"You've already go this in your list"
		))

	def test_error_massages_are_cleared_on_input(self):
		'''тест: сообщения об ошибках очищаются при вводе'''
		# Эдит начинает список и вызывает ошибку валидации:
		self.browser.get(self.live_server_url)
		self.add_list_item('Banter too thick')
		self.get_item_input_box().send_keys('Banter too thick')
		self.get_item_input_box().send_keys(Keys.ENTER)

		self.wait_for(lambda: self.assertTrue(
			self.get_error_element().is_displayed()
		))

		# Она начинает набирать в поле ввода, чтобы очистить ошибку
		self.get_item_input_box().send_keys('a')

		# Она довольна от того, что сообщение об ошибке исчезает
		self.wait_for(lambda: self.assertFalse(
			self.get_error_element().is_displayed()
		))
