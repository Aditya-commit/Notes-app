from .models import User,Note

from django import forms

class Userform(forms.ModelForm):
	class Meta:
		model=User
		fields=['username','name','email','password']

class LogForm(forms.Form):
	username=forms.CharField(max_length=40)
	password=forms.CharField(max_length=40,widget=forms.PasswordInput(attrs={'class' :'passwordinput'}))


