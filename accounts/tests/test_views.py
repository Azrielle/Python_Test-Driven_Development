from accounts.models import Token
from django.test import TestCase
from unittest.mock import patch , call
import accounts.views

@patch('accounts.views.auth')
class LoginViewTest(TestCase):

	def test_redirects_to_home_page(self, mock_auth):
		'''тест: переадресуется на домашнюю страницу'''
		responce = self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        })
		self.assertRedirects(responce, '/')

	def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
		'''тест: вызывается authenticate c uid из GET-запроса'''
		self.client.get('/accounts/login?token=adcd123')
		self.assertEqual(
			mock_auth.authenticate.call_args,
			call(uid='adcd123')
		)

	def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
		'''тест: вызывается auth_login с пользователем, если такой имеется'''
		responce = self.client.get('/accounts/login?token=adcd123')
		self.assertEqual(
			mock_auth.login.call_args,
			call(responce.wsgi_request, mock_auth.authenticate.return_value)
		)

	def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
		'''тест: не регистрируется в системе, если пользователь
		Не аутентифицирован'''
		mock_auth.authenticate.return_value = None
		self.client.get('/accounts/login?token=adcd123')
		self.assertEqual(mock_auth.login.called, False)

class SendLoginEmailViewTest(TestCase):
	'''тест представления, которое отправляет
	сообщение для входа в сиcтему'''

	

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
	