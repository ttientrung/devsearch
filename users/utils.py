from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProfiles(request, profiles, results):
    page = request.GET.get('page')
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    leftIndex = (int(page) - 2)
    if leftIndex < 1:
        leftIndex = 1

    righIndex = (int(page) + 3)
    if righIndex > paginator.num_pages:
        righIndex = paginator.num_pages + 1
    
    custom_range = range(leftIndex, righIndex)

    return profiles, custom_range

def searchProfiles(request):
    search_query = ''

    skill = Skill.objects.filter(name__icontains=search_query)

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query)|
        Q(skill__in=skill)|
        Q(short_intro__icontains=search_query))
    
    return profiles, search_query