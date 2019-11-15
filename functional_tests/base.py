import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class FunctionalTest(StaticLiveServerTestCase):
	'''функциональный тест'''

	def setUp(self):
		'''установка'''
		self.browser = webdriver.Firefox()
		staging_server = os.environ.get('STAGING_SERVER')
		if staging_server:
			self.live_server_url = 'http://' + staging_server

	def tearDown(self):
		'''демонтаж'''
		self.browser.quit()

	def wait_for_row_in_list_table(self,row_text):
		'''подтверждение строки в таблице списка'''
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

	def wait_for(self,fn):
		'''ожидать'''
		start_time = time.time()
		while True:
			try:
				return fn()
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

	def get_item_input_box(self):
		'''получить поле ввода для элемента'''
		return self.browser.find_element_by_id('id_text')

	def wait_to_be_logged_in(self, email):
		'''ожидать входа в систему'''
		self.wait_for(
			lambda: self.browser.find_element_by_link_text('Log out')
		)
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertIn(email, navbar.text)

	def wait_to_be_logged_out(self, email):
		'''ожидать выхода из системы'''
		self.wait_for(
			lambda: self.browser.find_element_by_name('email')
		)
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertNotIn(email, navbar.text)
