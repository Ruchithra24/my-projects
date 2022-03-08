from django.shortcuts import render,redirect
from .models import Profile,Message
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm 
from .forms import CustomUserCreationForm,ProfileForm,SkillForm,MessageForm
from django.contrib.auth.decorators import login_required
from .utils import searchProfiles,paginateProfiles
from django.db.models import Q

# Create your views here.

def profiles(request):
    profiles=searchProfiles(request)
    page_profiles,custom_range=paginateProfiles(request,profiles,1)
    
    
    context={
        'profiles':page_profiles,
        'custom_range':custom_range,
    }
    return render(request,'Users/all-profiles.html',context)

def profile(request,pk):
    profile=Profile.objects.get(id=pk)
    topSkill=profile.skill_set.exclude(description='')
    otherSkill=profile.skill_set.filter(description='')
    context={'profile':profile,
             'topskill':topSkill,'otherskill':otherSkill}
    return render(request,'Users/single-profile.html',context)

def loginUser(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('firstapp:project1')
    
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        try:
            user=User.objects.get(username=username)
        except:
            print('User does not exit')
        user=authenticate(username=username,password=password)
        
        if user is not None:
            print("User exist")
            login(request,user)
            messages.success(request,'user logged in Successfully')
            return redirect(request.GET['next'] if 'next' in request.GET else 'Users:account')
        else:
            messages.error(request,"username or password doesn't match")
    context={'page':page,}
    return render(request,'Users/login_register.html',context)
    
def logoutUser(request):
    logout(request)
    print('user logged out')
    return redirect('Users:login')
        
def registerUser(request):
    page='register'
    
    form=CustomUserCreationForm()
    
    if request.method=='POST':
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            messages.success(request,'User created Successfully')
            return redirect('Users:login')
        else:
            messages.error(request,'some error occured')
            
    context={'page':page,'form':form}
    return render(request,'Users/login_register.html',context)

@login_required(login_url='Users:login')
def userAccount(request):
    profile=request.user.profile
    
    context={'profile':profile}
    return render(request,'Users/account.html',context)


#@login_required(login_url='Users:login')
def editAccount(request):
    profile=request.user.profile
    form=ProfileForm(instance=profile)
    
    if request.method=='POST':
        form=ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,'profile updated successfully')
            return redirect('Users:account')
    
    context={'form':form}
    return render(request,'Users/edit_account.html',context)

@login_required(login_url='Users:login')
def createSkill(request):
    profile=request.user.profile
    form=SkillForm()
    
    if request.method=='POST':
        form=SkillForm(request.POST)
        if form.is_valid():
            skill=form.save(commit=False)
            skill.owner=profile
            skill.save()
            messages.success(request,'Skill created successfully')
            return redirect('Users:account')
        else:
            messages.error(request,'some error occured')
    context={'form':form}
    return render(request,'Users/skill-form.html',context)

        
@login_required(login_url='Users:login')
def updateSkill(request,pk):
    profile=request.user.profile
    skillobj=profile.skill_set.get(id=pk)
    
    form=SkillForm(instance=skillobj)
    if request.method=='POST':
        form=SkillForm(request.POST,instance=skillobj)
        if form.is_valid():
            form.save()
            messages.success(request,'skill updated successfully')
            return redirect(request,'Users:account')
        else:
            messages.error(request,'some error occured')
    
    context={'form':form}
    return render(request,'Users/skill-form.html',context)



@login_required(login_url='Users:login')
def deleteSkill(request,pk):
    profile=request.user.profile
    skillobj=profile.skill_set.get(id=pk)
    
    if request.method=='POST':
        skillobj.delete()
        messages.success(request,'skill deleted successfully')
        return redirect('Users:account')
    
    context={'object':skillobj}
    return render(request,'delete-template.html',context)
    
    

@login_required(login_url='Users:login')
def inbox(request):
    recipient = request.user.profile
    received_msgs = recipient.messages.all()
    unreadCount = received_msgs.filter(is_read=False).count()

    context = { 'received_msgs':received_msgs, 'unreadCount':unreadCount}
    return render(request,'Users/inbox.html',context)


@login_required(login_url='Users:login')
def viewMessage(request,pk):
    message = Message.objects.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()

    context = { 'message':message }
    return render(request,'Users/message.html',context) 


def createMessage(request,pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        try:
            sender = request.user.profile
        except:
            sender = None

        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient


            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()
            messages.success(request,'your message sent successfully')
            return redirect('Users:all-profile')

    context = {'form':form, 'recipient':recipient}                    
    return render(request,'Users/message-form.html',context)    


    
 
    