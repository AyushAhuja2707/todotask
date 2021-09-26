from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from ayush_final_project.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from random import randrange
from .models import *
from .forms import *
import requests

def dashboard(request):
    if request.user.is_authenticated:
        return render(request,'dashboard.html')
    else:
        redirect('user_login')

def home(request):
	return render(request,'home.html')

def signup(request):
    if request.method == 'POST':
        naam=request.POST.get('naam')
        un = request.POST.get('un')
        em = request.POST.get('em')
        try:
            usr = User.objects.get(username=un)
            return render(request,'signup.html',{'msg':'Username already exists '})
        except User.DoesNotExist:
            try:
                usr = User.objects.get(email=em)
                return render(request,"signup.html",{"msg":"Email already registered"})
            except User.DoesNotExist:
                pw=''
                text = "abcdefghijklmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ123456"
                for i in range(6):
                    pw =pw+text[randrange(len(text))]
                print(pw)
                msg = "Your Password is : "+pw
                send_mail("Welcome to Contact Ezre",msg,EMAIL_HOST_USER,[str(em)])
                usr=User.objects.create_user(username=un,password=pw,email=em)
                usr.save()
                return redirect("user_login")
    else:
        return render(request,'signup.html')
        

def user_login(request):
		
    if request.method =='POST':
        un= request.POST.get("un")
        pw= request.POST.get("pw")
        usr = authenticate(username = un,password = pw)
        if usr is None:
            return render(request,"user_login.html",{"msg":"Login is Denied"})
        
        else:
            login(request,usr)
            return redirect('dashboard')

    else:
        return render(request,"user_login.html")

def Logout(request):
	logout(request)
	return redirect('home')


def addtask(request):
	fm =TaskForm(request.POST)
	if request.method=='POST':
		
		t = request.POST.get("task")
		d=request.POST.get("due")
		ta = TaskModel.objects.create(task = t ,due=d, us = request.user)
		ta.save()
		return render(request,"addtask.html",{'fm':fm,"msg":"Task Added"})
	else:
		return render(request,"addtask.html",{"fm":fm})
		

def viewtask(request):
	if  request.user.is_authenticated:
		d = TaskModel.objects.filter(us=request.user)
		return render(request,"viewtask.html",{"data":d})
	else:
		return redirect('user_login')

def deletetask(request,id):	
    print(id)
    ds= TaskModel.objects.filter(id=id)
    ds.delete()
    return redirect('viewtask')
    
	#ds.delete()
	#return redirect('viewtask')

def weather(request):
    if request.GET.get("city"):
	    try:
		    city=request.GET.get("city")
		    a1="http://api.openweathermap.org/data/2.5/weather?units=metric"
		    a2="&q="+ city
		    a3="&appid="+"5c062c21f59edfdb5cbba1dd6c28138f"
		    wa=a1+a2+a3
		    res=requests.get(wa)
		    data=res.json()
		    temp=data['main']['temp']
		    return render(request,'weather.html',{"msg":temp})
	    except Exception:
		    return render(request,'weather.html',{"msg":"city name not found"})
	#return render(request,'home.html')
    return render(request,'weather.html')