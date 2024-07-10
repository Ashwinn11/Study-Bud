from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Rooms,Topic,Messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import RoomForm


def home(request):

    q=request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Rooms.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    topics = Topic.objects.all()
    room_count = rooms.count()
    context={'rooms':rooms,'topics':topics,'room_count':room_count}
    return render(request,'core/home.html',context)

def rooms(request,pk):
    rooms = Rooms.objects.get(id=pk)
    message=Messages.objects.filter(room=rooms).order_by('-created')

    if request.method=="POST":
        if request.POST.get('body')=="":
            messages.error(request,'The message cannot be empty')
            return redirect('room',pk=rooms.id)
        else:
            body = Messages.objects.create(user=request.user,body=request.POST.get('body'),room=rooms)
            body.save()
            return redirect('room',pk=rooms.id)

    context={'room':rooms,'message':message}
    return render(request,'core/room.html',context)


@login_required(login_url='login')
def createRoom(request):
    form=RoomForm()
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'core/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room =Rooms.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method=="POST":
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}    
    return render(request,'core/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Rooms.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'core/delete.html',{'obj':room})

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        username=request.POST.get('username').lower()
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'logged in')
            return redirect('home')
        else:
            messages.error(request,'user does not exist')
    context={}
    return render(request,'core/login_form.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    requestType='register'
    form = UserCreationForm()
    if request.method=="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"An error occurred during registration")
    
    context={'type':requestType,'form':form}
    return render(request,'core/login_form.html',context)