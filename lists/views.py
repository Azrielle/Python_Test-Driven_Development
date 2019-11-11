from django.core.exceptions import ValidationError
from django.shortcuts import render,redirect
from lists.forms import ItemForm
from lists.models import Item, List

# Create your views here.
def home_page(request):
	'''домашняя страница'''
	return render(request, 'home.html', {'form': ItemForm()})

def view_list(request, list_id):
	'''представление списка'''
	list_ = List.objects.get(id=list_id)
	form = ItemForm()
	if request.method == 'POST':
		form = ItemForm(data=request.POST)
		if form.is_valid():
			form.save(for_list=list_)
			return redirect(list_)
	return render(request, 'list.html', {'list': list_, "form":form})

def new_list(request):
	''' новый список '''
	form = ItemForm(data=request.POST)
	if form.is_valid():
		list_ = List.objects.create()
		form.save(for_list=list_)
		return redirect(list_)
	else:
		return render(request, 'home.html', {"form": form})
