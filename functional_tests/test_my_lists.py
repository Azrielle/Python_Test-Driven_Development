from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest

User = get_user_model()

class MyListsTest(FunctionalTest):
	'''тест ариложения "Мои списки"'''

	def create_pre_authenticated_session(self, email):
		'''создать предворительно аутентифицированный сеанс'''
		user = User.objects.create(email=email)
		session = SessionStore()
		session[SESSION_KEY] = user.pk
		session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
		session.save()
		## установить cookie, которые нужны для первого посещения домена.
		## страницы 404 загружаются быстрее всего!
		self.browser.get(self.live_server_url + "/404_no_such_url/")
		self.browser.add_cookie(dict(
			name=settings.SESSION_COOKIE_NAME,
			value=session.session_key,
			path='/'
		))

	def test_logged_in_users_lists_are_saved_as_my_lists(self):
		'''тест: списки зарегистрированных пользователей 
		сохраняются как "мои списки"'''
		email = 'edith@example.com'
		self.browser.get(self.live_server_url)
		self.wait_to_be_logged_out(email=email)

		# Эдит является зарегистрированным пользователем
		self.create_pre_authenticated_session(email)
		self.browser.get(self.live_server_url)
		self.wait_to_be_logged_in(email)