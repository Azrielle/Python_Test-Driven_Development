from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token

User = get_user_model()

class AuthenticateTest(TestCase):
	'''тест аутентификации'''

	def test_returns_None_if_no_surch_token(self):
		'''тест: возвращает None, если нет такого маркера'''
		result = PasswordlessAuthenticationBackend().authenticate(
			'no-such-token'
		)
		self.assertIsNone(result)

	def test_returns_new_user_with_correct_email_if_token_exists(self):
		'''тест: возвращается новый пользователь с правильной
		электроной почтой, если маркет существует'''
		email='edith@example.com'
		token = Token.objects.create(email=email)
		user = PasswordlessAuthenticationBackend().authenticate(token.uid)
		new_user = User.objects.get(email=email)
		self.assertEqual(user, new_user)

	def test_returns_existing_user_with_email_if_token_exists(self):
		'''тест: возвращается существующий пользователь с правильной 
		электроной почтой, если маркер существует'''
		email = 'edith@example.com'
		existing_user = User.objects.create(email=email)
		token = Token.objects.create(email=email)
		user = PasswordlessAuthenticationBackend().authenticate(token.uid)
		self.assertEqual(user, existing_user)