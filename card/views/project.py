from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.utils import timezone
from ..models import Project, Work, Minutes

from django.contrib.auth.decorators import login_required


@login_required(login_url='/card/login')
def index(request):
    user_id = request.user.id
    active_projects = Project.objects.order_by('name').filter(end_date__isnull=True, user_id=user_id)
    completed_projects = Project.objects.filter(end_date__isnull=False, user_id=user_id)
    context = {
        'projects': active_projects,
        'completed_projects': completed_projects
    }
    return render(request, 'card/project/index.html', context)

@login_required(login_url='/card/login')
def create(request):
    user_id = request.user.id
    p = Project(user_id=user_id, name=request.POST['name'], start_date=timezone.now())
    p.save()
    return HttpResponseRedirect(reverse('card:project'))

@login_required(login_url='/card/login')
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

@login_required(login_url='/card/login')
def destroy(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    return HttpResponseRedirect(reverse('card:project'))

@login_required(login_url='/card/login')
def complete(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.end_date = timezone.now()
    project.save()
    return HttpResponseRedirect(reverse('card:project'))
