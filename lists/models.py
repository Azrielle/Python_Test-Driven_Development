from django.db import models

# Create your models here.
class List(models.Model):
	''' список '''
	pass

class Item(models.Model):
	'''элемент списка'''
	text = models.TextField(default='')
	list = models.ForeignKey(List, default=None)

