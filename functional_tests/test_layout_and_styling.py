from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
	'''тест макета и стилевого оформления'''

	def test_layout_and_tyling(self):
		'''тест макета и стилевого оформления'''
		# Эдит открывает домашнюю страницу
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)

		# Она замечает, что поле ввода аккуратно центрованно
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=10
		)
		# Она начинает новый список и видит, что поле ввода там тоже
		# аккуратно центрованно
		inputbox.send_keys('testing')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: testing')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=10
		)

