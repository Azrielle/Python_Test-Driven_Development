from accounts.models import Token
from django.test import TestCase
from unittest.mock import patch
import accounts.views

class SendLoginEmailViewTest(TestCase):
	'''тест представления, которое отправляет
	сообщение для входа в сиcтему'''

	def test_redirects_to_home_page(self):
		'''тест: переадресуется на домашнюю страницу'''
		responce = self.client.get('/accounts/login?token=adcd123')
		self.assertRedirects(responce, '/')

	@patch('accounts.views.send_mail')
	def test_sends_mail_to_from_post(self, mock_send_mail):
		'''тест: отправляется сообщение на адрес из метода post'''
		self.client.post('/accounts/send_login_email', data={
			'email': 'edith@example.com'
		})

		self.assertEqual(mock_send_mail.called, True)
		(subject, body, from_email, to_list), kwargs = mock_send_mail.call_args

		self.assertEqual(subject, 'Your login link for Superlists')
		self.assertEqual(from_email, 'noreplay@superlists')
		self.assertEqual(to_list, ['edith@example.com'])

	def test_adds_success_message(self):
		'''тест: добовляется сообщение об успехе'''
		responce = self.client.post('/accounts/send_login_email', data={
			'email': 'edith@example.com'
		}, follow=True)

		message = list(responce.context['messages'])[0]
		self.assertEqual(
			message.message,
			"Проверте свою почту, мы отправили Вам ссылку, \
которую можно использовать для входа на сайт."
		)
		self.assertEqual(message.tags, "success")


	def test_creates_token_associated_with_email(self):
		'''тест: создается маркер, связанный с электронной почтой'''
		self.client.post('/accounts/send_login_email', data={
			'email': 'edith@example.com'
		})
		token = Token.objects.first()
		self.assertEqual(token.email, 'edith@example.com')

	@patch('accounts.views.send_mail')
	def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
		'''тест: отсылается ссылка на вход в систему, используя uid маркера'''
		self.client.post('/accounts/send_login_email', data={
			'email': 'edith@example.com'
		})

		token = Token.objects.first()
		expected_url = f'http://testserver/accounts/login?token={token.uid}'
		(subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
		self.assertIn(expected_url, body)