from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from .forms import *
import sys
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, authenticate

# Create your views here. 
@csrf_exempt
@login_required
def image_view(request): 

	if request.method == 'POST': 
		form = ImageForm(request.POST, request.FILES) 
		if request.user.is_authenticated:
			user = request.user
		if form.is_valid(): 
			form.instance.user = user
			form.save()
			return redirect('gallery') 
	else: 
		form = ImageForm() 
	return render(request, 'image_upload.html', {'form' : form}) 

@csrf_exempt
@login_required
def display_images(request): 

	if request.method == 'GET': 
		if request.user.is_authenticated:
			user = request.user
		Images = Image.objects.filter(user=user)
		public_images = Image.objects.filter(user=get_user_model().objects.get(username='admin'))
		combined_images = Images | public_images
		return render(request, 'images_display.html', {'images' : combined_images, 'public_images' : public_images, 'private_images' : Images, 'user' : user.username })
	if request.method == 'POST':
		if request.POST.get('delete_btn'):
			Image.objects.filter(id=request.POST.get('delete_btn')).delete()
		if request.user.is_authenticated:
			user = request.user
		Images = Image.objects.filter(user=user)
		public_images = Image.objects.filter(user=get_user_model().objects.get(username='admin'))
		combined_images = Images | public_images
		return render(request, 'images_display.html', {'images' : combined_images, 'public_images' : public_images, 'private_images' : Images, 'user' : user.username})
		
	

@csrf_exempt
def create(request):
	if request.method == 'POST': 
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password')
			auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
			return redirect('gallery') 
	else: 
		form = UserCreationForm() 
	return render(request, 'create_user.html', {'form' : form}) 

@csrf_exempt
def login(request):
	if request.method == 'POST': 
		form = UserForm(request.POST) 
		if form.is_valid(): 
			
			return redirect('gallery') 
	else: 
		form = UserForm() 
	return render(request, 'login.html', {'form' : form}) 

@csrf_exempt	
def success(request): 
	return HttpResponse('successfully uploaded') 
