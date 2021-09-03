from django.contrib import admin
from django.urls import path
from . import views

urlpatterns=[
	path('',views.index , name='index'),
	path('create/',views.create,name='create'),
	path('login/',views.login,name='login'),
	path('display/',views.display,name='display'),
	path('delete/<int:id>/' , views.delete,name='delete'),
	path('logout/',views.logout , name='logout'),
]