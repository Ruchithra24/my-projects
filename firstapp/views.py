from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Project
from .models import Review
from .models import Tag
from .forms import ProjectForm,ReviewForm
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.db.models import Q
from .utils import searchProjects,paginateProjects


# Create your views here.
def project1(request):
    projects=searchProjects(request)
    page_projects,custom_range=paginateProjects(request,projects,1)

    context={
         'keyname': page_projects,
         'custom_range':custom_range
    }  
    return render(request,'firstapp/projects.html',context)


    
def project(request,pk):
    proj_obj=Project.objects.get(id=pk)

    tags= proj_obj.tags.all()
    
    reviews=proj_obj.review_set.all()
    form=ReviewForm()
    
    if request.method=="POST":
        form=ReviewForm(request.POST)
        if form.is_valid():
            review=form.save(commit=False)
            review.project=proj_obj
            review.owner=request.user.profile
            review.save()
            
            proj_obj.getVoteCount 
            
            messages.success(request,'Your review was submitted successfully')
            return redirect('firstapp:project',pk=proj_obj.id)

        else:
            messages.error(request,"some error occured")
    
    context={"proj":proj_obj,'tags':tags,'reviews':reviews,'form':form
    }
    return render(request,'firstapp/project.html',context)

@login_required(login_url='Users:login')
def createProject(request):
    profile=request.user.profile
    form=ProjectForm()
    
    if request.method=='POST':
        form=ProjectForm(request.POST,request.FILES)

        if form.is_valid():
            project=form.save(commit=False)
            project.owner=profile
            project.save()
            return redirect('Users:account')

    context={'form':form,}
    return render(request,'firstapp/project-form.html',context)

@login_required(login_url='Users:login')
def updateProject(request,pk):
    profile=request.user.profile
    projectObj=profile.project_set.get(id=pk)
    form=ProjectForm(instance=projectObj)

    if request.method =='POST':
        form=ProjectForm(request.POST,instance=projectObj)
        if form.is_valid():
            form.save()
            messages.success(request,"Project updated successfully")
            return redirect('Users:account')

    context={'form':form,}
    return render(request,'firstapp/project-form.html',context)

@login_required(login_url='Users:login')
def deleteProject(request,pk):
    profile=request.user.profile
    projObj=profile.project_set.get(id=pk)
    

    if request.method =='POST':
        projObj.delete()
        messages.success(request,"Project deleted successfully")
        return redirect('Users:account')

    context={'object':projObj,}
    return render(request,'delete-template.html',context)

