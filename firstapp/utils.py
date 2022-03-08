from .models import Tag,Project
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def searchProjects(request):
    search_query=''
    if request.GET.get('search_query'):
        search_query=request.GET['search_query']
        
    tags=Tag.objects.filter(name__icontains=search_query)
    
    projects=Project.objects.filter(Q(title__icontains=search_query)|
                                    Q(owner__name__icontains=search_query)|
                                    Q(tags__in=tags)).distinct()    
    return projects


def paginateProjects(request,keyname,no_of_proj):
    paginator=Paginator(keyname,no_of_proj)
    
    page=request.GET.get('page')
    try:
        page_projects=paginator.page(page)
    except PageNotAnInteger:
        page=1
        page_projects=paginator.page(page)
    except EmptyPage:
        page=paginator.num_pages
        page_projects=paginator.page(page)
     
    leftIndex=int(page) - 2 
    if leftIndex<1:
        leftIndex=1
    
    rightIndex=int(page)+2
    if rightIndex>paginator.num_pages:
        rightIndex=paginator.num_pages+1
    
    custom_range=range(leftIndex,rightIndex)
       
    return page_projects,custom_range

