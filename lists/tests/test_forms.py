from django.test import TestCase
from lists.forms import (
	DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR,
	ExistingListItemForm, ItemForm
)
from lists.models import Item, List

class ItemFormTest(TestCase):
	'''тест формы для элемента списка'''

	def test_form_render_item_text_input(self):
		'''тест: форма отображает текстовое поле ввода'''
		form = ItemForm()
		self.assertIn('placeholder="Enter a to-do item"', form.as_p())
		self.assertIn('class="form-control input-lg"', form.as_p())

	def test_form_validation_for_blank_items(self):
		'''тест валидации формы для пустых элементов'''
		form = ItemForm(data={'text': ''})
		self.assertFalse(form.is_valid())
		self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])
		
	def test_form_save_handles_saving_to_a_list(self):
		'''тест: метод save формы обрабатывает сохранение в список'''
		list_ = List.objects.create()
		form = ItemForm(data={'text': 'do me'})
		new_item = form.save(for_list=list_)
		self.assertEqual(new_item, Item.objects.first())
		self.assertEqual(new_item.text, 'do me')
		self.assertEqual(new_item.list, list_)

class ExistingListItemFormTest(TestCase):
	'''тест формы элемента существующего списка'''

	def test_form_renders_item_text_input(self):
		'''тест: форма отображает текстовый ввод элемента'''
		list_ = List.objects.create()
		form = ExistingListItemForm(for_list=list_)
		self.assertIn('placeholder="Enter a to-do item"', form.as_p())

	def test_form_validation_for_blank_items(self):
		'''тест: валидация формы для пустых элементов'''
		list_ = List.objects.create()
		form = ExistingListItemForm(for_list=list_, data={'text': ''})
		self.assertFalse(form.is_valid())
		self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

	def test_form_validation_for_dublocate_items(self):
		'''тест: валидация формы для повторных элементов'''
		list_ = List.objects.create()
		Item.objects.create(list=list_, text='no twins!')
		form = ExistingListItemForm(for_list=list_, data={'text': 'no twins!'})
		self.assertFalse(form.is_valid())
		self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

	def test_form_save(self):
		'''туст сохранение формы'''
		list_ = List.objects.create()
		form = ExistingListItemForm(for_list=list_, data={'text': 'hi'})
		new_item = form.save()
		self.assertEqual(new_item, Item.objects.all()[0])