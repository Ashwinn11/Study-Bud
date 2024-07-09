from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Rooms
from .forms import RoomForm



def home(request):
    rooms = Rooms.objects.all()
    context={'rooms':rooms}
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
