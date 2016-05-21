from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.utils import timezone
from ..models import Project, Work, User


def index(request):
    active_projects = Project.objects.order_by('-name').filter(end_date__isnull=True)
    completed_projects = Project.objects.filter(end_date__isnull=False)
    context = {
        'projects': active_projects,
        'completed_projects': completed_projects
    }
    return render(request, 'card/project/index.html', context)


def create(request):
    # user id = 2 until logging in implemented
    p = Project(user_id=2, name=request.POST['name'], start_date=timezone.now())
    p.save()
    return HttpResponseRedirect(reverse('card:project'))


def show(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.end_date is None:
        completed = False
    else:
        completed = True
    context = {
        'project': project,
        'completed': completed
    }
    return render(request, 'card/project/show.html', context)


def destroy(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    return HttpResponseRedirect(reverse('card:project'))


def complete(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.end_date = timezone.now()
    project.save()
    return HttpResponseRedirect(reverse('card:project'))
