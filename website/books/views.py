from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login
from django.http import HttpResponse

def index(request):
	if request.method=='POST':
		form=AuthenticationForm(request,request.POST)
	return render(request, "index.html")
