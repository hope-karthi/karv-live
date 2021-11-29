from django import forms
from django.shortcuts import redirect, render
from django.db.models import Q
from .models import Room, Topic, Message
from .models import User as U
from .forms import RoomForm, UserForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages #msg are sent to main.html
from django.contrib.auth import authenticate,login,logout
from .forms import MyUserCreationForm as UserCreationForm
from django.http import HttpResponse


def loginPage(request):
    page='login'#'login_register.html' have login & register form to use if else to separate the forms

    if request.user.is_authenticated:#if user already login then he can't login
        messages.error(request,"Please Logout '_'")
        return redirect('datas')
    
    if request.method=='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')

        try:#for check user exist or not
            user=U.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')
        user=authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('datas')
        else:
            messages.error(request,'Username or Password does not exit')            
    context={'page':page}
    return render(request,'baseapp/login_register.html',context) 

def logoutPage(request):
    logout(request)
    return redirect('datas')

def registerPage(request):
    form=UserCreationForm()
    
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request, user)
            return redirect('datas')
        else:
            messages.error(request, 'An error Required during registration')
            
    context={'form':form}
    return render(request,'baseapp/login_register.html',context)

    

def home(request):
    queue=request.GET.get('q') if request.GET.get('q') !=None else '' #for search bar
    #q is use in data.html for "href" tag and get value of 'q'
    #"if request.GET.get('q') !=None else '' "--This will show all rooms in the DB
    datas=Room.objects.filter(
        Q(topic__name__icontains=queue) | #"icontains"--This is for user search relate to topic name & it will show result
        Q(name__icontains=queue) |
        Q(description__icontains=queue)
        )
    all_room=Room.objects.all()
    #topic__name is called Topic is query upward to the parent
    #(we access room obj, room have name & topic also have name) so "__"(double underscore)
    topic=Topic.objects.all()[0:4]
    count=datas.count()
    room_message=Message.objects.filter(Q(room__topic__name__icontains=queue))[0:5]
    context={'datas':datas,'topic':topic,'count':count,'room_message':room_message,'all_room':all_room}
    return render(request,'baseapp/data.html',context)

def RoomPage(request,pk):
    room=Room.objects.get(id=pk)
    room_messages = room.message_set.all()#set of messages related to specific room
    participants=room.participants.all()
    if request.method == 'POST':
        messages=Message.objects.create(##for save and show the comment msg
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)#if user2 is comment then he is participate
        return redirect('room',pk=room.id)#room url have pk value so we specify pk
    context={'data':room, 'room_messages':room_messages,'participants':participants}
    return render(request,'baseapp/room.html',context)

def userProfile(request,pk):
    user=U.objects.get(id=pk)
    room=user.room_set.all()
    room_message =user.message_set.all()
    topic=Topic.objects.all()
    context={'user':user,'datas':room,'topic':topic,'room_message':room_message}
    return render(request,'baseapp/profile.html',context)


@login_required(login_url='login')
def createRoom(request):
    forms=RoomForm()
    topics=Topic.objects.all()
    if request.method =='POST':
        topic_name=request.POST.get('topic')
        topic, created=Topic.objects.get_or_create(name=topic_name)#if topic is not in listof topic then create new one
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('home_page')
    context={'form':forms,'topic':topics}
    return render(request,'baseapp/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    topics=Topic.objects.all()
    room=Room.objects.get(id=pk)
    forms=RoomForm(instance=room)
    if request.user != room.host:#eg:user:'karthi' is allow to edit his room but not allow to another user
        return HttpResponse("You are not allowed..!")
    if request.method =='POST':
        form=RoomForm(request.POST, instance=room)
        topic_name=request.POST.get('topic')
        topic, created=Topic.objects.get_or_create(name=topic_name)
        room.name=room.POST.get('name')
        room.topic=topic     
        room.description=room.POST.get('description')
        room.save()
        return redirect('home_page')
    context={'topic':topics,'form':forms,}
    return render(request, 'baseapp/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room=Room.objects.get(id=pk)
    if request.user != room.host:#eg:user:'karthi' is allow to edit his room but not allow to another user
        return HttpResponse("You are not allowed..!")
    if request.method == 'POST':
        room.delete()
        return redirect('home_page')
    return render(request,'baseapp/delete.html',{'obj':room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message=Message.objects.get(id=pk)
    if request.user != message.user:#eg:user:'karthi' is allow to edit his room but not allow to another user
        return HttpResponse("You are not allowed..!")
    if request.method == 'POST':
        message.delete()
        return redirect('home_page')
    return render(request,'baseapp/delete.html',{'obj':message})


@login_required(login_url='login')
def updateUser(request):
    user=request.user
    form =UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('userprofile',pk=user.id)

    context={'form':form}
    return render(request, 'baseapp/updateuser.html', context) 

def topicsPage(request):
    queue=request.GET.get('q') if request.GET.get('q') !=None else ''
    topic=Topic.objects.filter(name__icontains=queue)
    datas=Room.objects.all
    context={'topic':topic,'datas':datas}
    return render(request,'baseapp/topics.html',context)

def activityPage(request):
    room_message=Message.objects.all()
    context={'room_message':room_message}
    return render(request,'baseapp/activity.html',context)