# forms.py 
from django import forms 
from .models import *
from django.contrib.auth import get_user_model

class ImageForm(forms.ModelForm): 
	class Meta: 
		model = Image 
		fields = ['image_name', 'image_file'] 

class UserForm(forms.ModelForm):
	class Meta:
		model = get_user_model()
		fields = ['username', 'password']