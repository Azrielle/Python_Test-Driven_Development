from django import forms
from lists.models import Item
from django.core.exceptions import ValidationError
from lists.models import Item, List

EMPTY_ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already go this in your list"

class ItemForm(forms.models.ModelForm):
	'''форма для элемента списка'''

	class Meta:
		model = Item
		fields = ('text',)
		widgets = {
			'text': forms.fields.TextInput(attrs={
				'placeholder': 'Enter a to-do item',
				'class': 'form-control input-lg',
			}),
		}
		error_messages = {
			'text': {'required': EMPTY_ITEM_ERROR}
		}

class NewListForm(ItemForm):
	'''форма для нового списка'''
	def save(self, owner):
		if owner.is_authenticated:
			return List.create_new(first_item_text=self.cleaned_data['text'],
			owner=owner)
		else:
			return List.create_new(first_item_text=self.cleaned_data['text'])

class ExistingListItemForm(ItemForm):
	'''форма для элемента существующего списка'''
	def __init__(self, for_list, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.instance.list = for_list

	def validate_unique(self):
		'''проверка уникальности'''
		try:
			self.instance.validate_unique()
		except ValidationError as e:
			e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
			self._update_errors(e)
