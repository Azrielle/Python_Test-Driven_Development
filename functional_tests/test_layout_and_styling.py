from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from .list_page import ListPage

class LayoutAndStylingTest(FunctionalTest):
	'''тест макета и стилевого оформления'''

	def test_layout_and_tyling(self):
		'''тест макета и стилевого оформления'''
		# Эдит открывает домашнюю страницу
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)

		# Она замечает, что поле ввода аккуратно центрованно
		list_page = ListPage(self)
		inputbox = list_page.get_item_input_box()
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=10
		)
		# Она начинает новый список и видит, что поле ввода там тоже
		# аккуратно центрованно
		list_page.add_list_item('testing')
		inputbox = list_page.get_item_input_box()
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=10
		)

