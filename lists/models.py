from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings

# Create your models here.
class List(models.Model):
	''' список '''
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
	def get_absolute_url(self):
		'''получить абсолютный url'''
		return reverse('view_list', args=[self.id])
	
	@staticmethod
	def create_new(first_item_text, owner=None):
		'''создать новый'''
		list_ = List.objects.create(owner=owner)
		Item.objects.create(text=first_item_text, list=list_)
		return list_
	
	@property
	def name(self):
		return self.item_set.first().text

class Item(models.Model):
	'''элемент списка'''
	text = models.TextField(default='')
	list = models.ForeignKey(List, default=None)

	class Meta:
		ordering = ('id',)
		unique_together = ('list', 'text')

	def __str__(self):
		return self.text

