from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Rooms,Topic,Messages,User
from django.contrib.auth import authenticate,login,logout
from .forms import RoomForm,UserForm,MyUserCreationForm


def home(request):

    q=request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Rooms.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_msg=Messages.objects.filter(Q(room__topic__name__icontains=q))
    context={'rooms':rooms,'topics':topics,'room_count':room_count,'room_msg':room_msg}
    return render(request,'core/home.html',context)

def rooms(request,pk):

    rooms = Rooms.objects.get(id=pk)
    message=Messages.objects.filter(room=rooms)
    participants=rooms.participants.all()
    if request.method=="POST":
        if request.POST.get('body')=="":
            messages.error(request,'The message cannot be empty')
            return redirect('room',pk=rooms.id)
        else:
            body = Messages.objects.create(user=request.user,body=request.POST.get('body'),room=rooms)
            rooms.participants.add(request.user)
            return redirect('room',pk=rooms.id)

    context={'room':rooms,'message':message,'participants':participants}
    return render(request,'core/room.html',context)

def loginPage(request):

    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username/Password does not exit')
    context={}
    return render(request,'core/login_form.html',context)

def logoutUser(request):

    logout(request)
    return redirect('home')

def registerUser(request):

    requestType='register'
    form = MyUserCreationForm()
    if request.method=="POST":
        form = MyUserCreationForm(request.POST)
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


def userProfile(request,pk):

    user = User.objects.get(id=pk)
    rooms=Rooms.objects.filter(host=user)
    room_msg = Messages.objects.filter(user=user)
    topics= Topic.objects.all()
    context={'user':user,'rooms':rooms,"room_msg":room_msg,"topics":topics}
    return render(request,'core/profile.html',context)

@login_required(login_url='login')
def updateUser(request):

    user=request.user
    form = UserForm(instance=user)
    if request.method=='POST':
        form = UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)
    context={'form':form}
    return render(request,'core/update-user.html',context)


@login_required(login_url='login')
def createRoom(request):

    topics= Topic.objects.all()
    form=RoomForm()
    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        Rooms.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    context={'form':form,'topics':topics}
    return render(request,'core/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):

    topics= Topic.objects.all()
    room =Rooms.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method=="POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context={'form':form,'topics':topics,'room':room}    
    return render(request,'core/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):

    room = Rooms.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'core/delete.html',{'obj':room})

def deleteMessage(request,pk):

    message = Messages.objects.get(id=pk)
    roomId=message.room.id
    if request.method=='POST':
        message.delete()
        return redirect('room',pk=roomId)
    context={'obj':message}
    return render(request,'core/delete.html',context)

def topicsPage(request):

    q=request.GET.get('q') if request.GET.get('q') != None else ''
    topics=Topic.objects.filter(name__icontains=q)
    context={'topics':topics}
    return render(request,'core/topic-page.html',context)

def activityPage(request):

    room_messages = Messages.objects.all()
    return render(request, 'core/activity-page.html', {'room_messages': room_messages})