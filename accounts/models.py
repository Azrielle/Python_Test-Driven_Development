from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager, PermissionsMixin
)

class ListUserManager(BaseUserManager):
	'''менеджер пользователя списка'''

	def create_user(self, email):
		'''создать пользователя'''
		ListUser.objects.create(email=email)

	def create_superuser(self, email, password):
		'''создать суперпользователя'''
		self.create_user(email)

class ListUser(AbstractBaseUser, PermissionsMixin):
	'''пользователь списка'''
	email = models.EmailField(primary_key=True)
	USERNAME_FIELD = 'email'
	# REQUIRED_FIELDS = ['email', 'height']

	objects = ListUserManager()

	@property
	def is_staff(self):
		return self.email == 'harry.percival@example.com'

	@property
	def is_active(self):
		return True
	
	
class Token(models.Model):
	'''маркер'''
	email = models.EmailField()
	uid = models.CharField(max_length=255)

