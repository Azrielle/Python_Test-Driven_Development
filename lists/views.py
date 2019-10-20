from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request):
	'''домашняя страница'''
	return HttpResponse('<html><title>To-Do</title></html>')
