from django.db import models

# Create your models here.

class Note(models.Model):
	username=models.ForeignKey('User',on_delete=models.CASCADE)
	title=models.TextField()
	text=models.TextField()

	def __str__(self):
		return f'{self.username}'

class User(models.Model):
	username=models.CharField(max_length=40,primary_key=True)
	name=models.CharField(max_length=40)
	email=models.EmailField()
	password=models.CharField(max_length=40)

	def __str__(self):
		return f'{self.username}'


