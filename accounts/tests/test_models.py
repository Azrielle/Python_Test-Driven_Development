from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Token

User = get_user_model()

class UserModelTest(TestCase):
	'''тест модели пользователя'''

	def test_user_is_valid_with_email_only(self):
		'''тест: пользователь с допустим только с электроной почтой'''
		user = User(email="a@b.com")
		user.full_clean() # не должно поднять исключение

	def test_email_is_primary_key(self):
		'''темт: адрес электронной почты является первичным ключом'''
		user = User(email='a@b.com')
		self.assertEqual(user.pk, 'a@b.com')

class TokeModelTest(TestCase):
	'''тест модели маркера'''

	def test_links_user_with_auto_generated_uid(self):
		'''тест: соединяет пользователя с автосгенерированным uid'''
		token1 = Token.objects.create(email='a@b.com')
		token2 = Token.objects.create(email='a@b.com')
		self.assertNotEqual(token1.uid, token2.uid)