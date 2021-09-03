from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from .models import User,Note
from .forms import Userform,LogForm
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def index(request):

	if request.method=="GET":
		owner=request.session.get('owner','has_expired')

		if owner=='has_expired':
			return HttpResponseRedirect('/login/')

		else:

			if cache.get('user','has_expired')=='has_expired':
				id_list=[]
				title_list=[]
				text_list=[]

				for i in Note.objects.values('id','title','text').filter(username=request.session['owner']):
					id_list.append(i['id'])
					title_list.append(i['title'])
					text_list.append(i['text'])

				cache.set_many({'id':id_list ,  request.session['owner']:request.session['owner'] , 'titles':title_list , 'texts':text_list})

				return render(request,'index.html')

			else:
				c=cache.get('user')
				return render(request,'index.html')

def create(request):
	if request.method=='GET':
		form=Userform()
		return render(request,'create.html',{'form':form})

	elif request.method=='POST':
		data=Userform(request.POST)
		
		if data.is_valid():
			username=data.cleaned_data['username']
			name=data.cleaned_data['name']
			email=data.cleaned_data['email']
			password=data.cleaned_data['password']

			if User.objects.filter(username=username,password=password).exists():
				return render(request,'create.html' , {'data':data})

			user=User(username=username,name=name,email=email,password=password)
			user.save()

			request.session['owner']=username
			return HttpResponseRedirect('/')

		else:
			return render(request,'create.html',{'form':data})

def login(request):

	if request.method=='GET':
		owner = request.session.get('owner','has_expired')
		if owner == 'has_expired':
			form=LogForm()
			return render(request,'login.html',{'form':form})

		else:
			return HttpResponseRedirect('/')

	elif request.method=='POST':
		data=LogForm(request.POST)
		print('Eneterd post')
		if data.is_valid():
			username=data.cleaned_data['username']
			password=data.cleaned_data['password']

			if User.objects.filter(pk=username,password=password).exists():
				request.session['owner']=username

				return HttpResponseRedirect("/")
			
			else:
				return render(request, 'login.html',{'form':data})
		else:
			print(data)

			return render(request,'login.html',{'form':data})

# @csrf_exempt
def display(request):

	if request.method=='GET':

		value=cache.get(request.session['owner'] , 'has_expired')
		
		if value == 'has_expired':
			id_list=[]
			title_list=[]
			text_list=[]

			data = Note.objects.values('id','title', 'text').filter(username=request.session['owner'])

			if len(data)!=0:
				for i in data :
					id_list.append(i['id'])
					title_list.append(i['title'])
					text_list.append(i['text'])

				cache.set_many({'id':id_list,request.session['owner']: request.session['owner'] , 'titles':title_list,'texts':text_list})

				return HttpResponse(json.dumps({'id':id_list,'title':title_list , 'text':text_list}))

			else:
				return HttpResponse('no data available')

		else:		

			return HttpResponse(json.dumps({'id':cache.get('id'),'title':cache.get('titles') ,'text' :cache.get('texts')}))

	elif request.method=='POST':

		data=json.loads(request.body)

		note=User.objects.values('username' , 'name','email','password').filter(username=request.session['owner'])

		mylit=iter(note)
		nextiter=next(mylit)
		userinstance=User(username=request.session['owner'], name=nextiter['name'] , email=nextiter['email'],password=nextiter['password'])

		noteinst=Note(username=userinstance , title=data['title'] , text=data['text'])

		noteinst.save()

		if cache.get(request.session['owner'] , 'has_expired')!='has_expired':
			
			id_list=cache.get('id')
			title_list = cache.get('titles')
			text_list=cache.get('texts')

			last=Note.objects.latest('id')

			id_list.append(last.id)

			title_list.append(data['title'])
			text_list.append(data['text'])

			cache.delete_many(['id','user','titles','texts'])
			cache.set_many({'id': id_list ,request.session['owner']: request.session['owner'] , 'titles':title_list,'texts':text_list})

			return HttpResponse(json.dumps({'status':200 , 'id':id_list[-1] , 'noteno':len(title_list)}))


def delete(request,id):

	a=Note.objects.get(pk=id)
	a.delete()

	cache.delete_many([request.session['owner'],'titles','texts'])

	return HttpResponseRedirect('/')


def logout(request):

	request.session.flush()

	return HttpResponseRedirect('/login/')
