from django.shortcuts import render, redirect
from .models import Post, Profile, IP, Flag, Session
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import codecs
import random
from django.contrib.auth import logout
import datetime

def is_fake(username):
    try:
        username.groups.get(name="FakeAdmin")
        return False
    except:
        return True

def get_users():
    users = User.objects.filter(is_staff=False)
    users = list(filter(is_fake,users))
    return users

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Create your views here.
def index(request):    
    return render(request, 'xss/base.html', )


def logout_view(request):
    logout(request)
    return redirect('/xss')


@login_required(login_url='../../register/login')
def admin_panel(request):
    context = {}
    users = get_users()
    context['users'] = users
    return render(request, 'xss/admin_panel.html', context)


@login_required(login_url='../../register/login')
def test(request):
    if request.method == 'POST':
        f = open("tests.txt","a+")
        data = request.POST.get('post','')
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip = get_client_ip(request)
        f.write(data + ":" + ip + ":" + request.user.username + ":" + time + "\n")
        user = User.objects.get(pk=request.user.id)
        # messages.set_level(request, messages.DEBUG)
        print(data)
        messages.success(request, data)
        # context = {'messages': messages}
        return render(request, 'xss/test.html',)
    else:
        return render(request, 'xss/test.html', )

@login_required(login_url='../../register/login')
def admin(request):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    f = open("flags.txt","a+")
    flag = random.getrandbits(128)
    sessid = request.COOKIES.get('sessionid')
    user = Session.objects.get(number=sessid).user
    f2 = Flag(user=user, name=flag)
    f2.save()
    ip = get_client_ip(request)
    f.write(str(flag) + ":" + ip + ":"  + request.user.username + ":" + time + "    \n")
    context = dict(flag=flag)
    return render(request, 'xss/admin.html', context)


@login_required(login_url='../../register/login')
def view_profiles(request):
    user_list = User.objects.all()
    context = {'users':user_list}
    if request.method == 'POST':
        data = request.POST.get('post','')
        data = data[2:-1]
        data = codecs.decode(data,"hex")
        data = data.decode("utf-8")
        messages.success(request, data)
        # context = {'messages': messages}
        return render(request, 'xss/viewprofiles.html', context)
    else:
        return render(request, 'xss/viewprofiles.html', context)

@login_required(login_url='../../register/login')
def profile(request):
    f = open("users.txt","a+")
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = get_client_ip(request)
    f.write(ip + ":" + request.user.username + ":" + time + "\n")
    user = User.objects.get(pk=request.user.id)
    try:
        bio = user.profile.bio
    except:
        bio = 'You have not created a profile yet. Create one below. Be sure to test what it looks like before you post it.'
    
    context = dict(bio=bio)
    
    return render(request, 'xss/profile.html',context)

@login_required(login_url='../../register/login')
def update_bio(request):
    user = User.objects.get(pk=request.user.id)

    if request.method == 'POST':

        data = request.POST.get('bio','')
        print(data)

        updates = {'bio': data}
        #Updates user or creates a user with default's settings
        Profile.objects.update_or_create(user=user, defaults=updates)
        IP.objects.get_or_create(user=user, number=get_client_ip(request))


        return redirect('/xss/profile')
    
    else:
        return render(request, 'xss/updatebio.html')