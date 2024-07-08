from django.shortcuts import render
from django.http import HttpResponse
from .models import Rooms

def home(request):
    rooms = Rooms.objects.all()
    context={'rooms':rooms}
    return render(request,'main.html',context)

def rooms(request,pk):

    rooms = Rooms.objects.get(id=pk)
    return render(request,'core/home.html',{'room':rooms})