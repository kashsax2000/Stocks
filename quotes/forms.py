from django import forms
from .models import Stock
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class StockForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ["ticker"]

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username','email','password1','password2']