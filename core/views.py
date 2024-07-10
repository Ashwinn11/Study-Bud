from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from .models import Rooms,Topic
from django.contrib.auth import authenticate,login,logout
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
    return render(request,'core/room.html',{'room':rooms})

def createRoom(request):

    form=RoomForm()
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'core/room_form.html',context)

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

def deleteRoom(request,pk):
    room = Rooms.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'core/delete.html',{'obj':room})

def loginPage(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,'logged in')
                return redirect('home')
        except:
            messages.error(request,'user does not exist')
    context={}
    return render(request,'core/login_form.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')
