from django.shortcuts import render,redirect
from lists.models import Item, List

# Create your views here.
def home_page(request):
	'''домашняя страница'''
	return render(request, 'home.html')

def view_list(request):
	'''представление списка'''
	items = Item.objects.all()

	return render(request, 'list.html',{'items': items})

def new_list(request):
	''' новый список '''
	list_ = List.objects.create()
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect('/lists/one-list-world/')