from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from datetime import datetime
from django.utils import timezone
from ..models import Project, Work, Minutes

from django.contrib.auth.decorators import login_required


@login_required(login_url='/card/login')
def start_new_work(request, project_id):
    # Get start time from GET-parameters
    start_hour = int(request.GET.get("start_hour"))
    start_minute = int(request.GET.get("start_minute"))
    start_time = datetime.now().replace(hour=start_hour, minute=start_minute)
    # start_time = timezone.localtime(start_time)

    project = get_object_or_404(Project, pk=project_id)
    # Start timers only for active projects
    if (project.end_date is None):
        user_id = request.user.id
        project.work_set.create(user_id=user_id, start_time=start_time)
    return HttpResponseRedirect(reverse('card:index'))

@login_required(login_url='/card/login')
def done(request, work_id):
    work = get_object_or_404(Work, pk=work_id)
    work.end_time = timezone.now()
    work.save()
    return HttpResponseRedirect(reverse('card:index'))

@login_required(login_url='/card/login')
def add(request):
    user_id = request.user.id
    active_projects = Project.objects.order_by('name').filter(end_date__isnull=True, user_id=user_id)
    return render(request, 'card/work/add.html', {"projects": active_projects})

@login_required(login_url='/card/login')
def add_new_work(request):
    user_id = request.user.id
    project_id = request.POST['project_id']
    start_time = request.POST['start_time']
    end_time = request.POST['end_time']

    try:
        work = Work(project_id=project_id, user_id=user_id, start_time=start_time, end_time=end_time)
        work.save()
        return HttpResponseRedirect(reverse('card:history'))
    except:
        active_projects = Project.objects.order_by('name').filter(end_date__isnull=True, user_id=user_id)

        context = {
            "projects": active_projects,
            "error": "Date was given incorrectly.",
            "start_time": start_time,
            "end_time": end_time,
            "project_id": int(project_id)
        }

        return render(request, 'card/work/add.html', context)

@login_required(login_url='/card/login')
def edit(request, work_id):
    work = get_object_or_404(Work, pk=work_id)
    user_id = request.user.id
    active_projects = Project.objects.order_by('name').filter(end_date__isnull=True, user_id=user_id)

    context = {
        "projects": active_projects,
        "start_time": work.start_time,
        "end_time": work.end_time,
        "project_id": work.project_id,
        "work_id": work.id
    }

    return render(request, 'card/work/edit.html', context)

@login_required(login_url='/card/login')
def update(request, work_id):
    user_id = request.user.id
    work = get_object_or_404(Work, pk=work_id)
    project_id = request.POST['project_id']
    start_time = request.POST['start_time']
    end_time = request.POST['end_time']

    try:
        work.project_id = project_id
        work.start_time = start_time
        work.end_time = end_time
        work.save()
        return HttpResponseRedirect(reverse('card:history'))
    except:
        active_projects = Project.objects.order_by('name').filter(end_date__isnull=True, user_id=user_id)

        context = {
            "error": "Date was given incorrectly.",
            "projects": active_projects,
            "start_time": start_time,
            "end_time": end_time,
            "project_id": int(project_id),
            "work_id": work_id
        }

        return render(request, 'card/work/edit.html', context)

@login_required(login_url='/card/login')
def delete(request, work_id):
    work = get_object_or_404(Work, pk=work_id)
    work.delete()
    return HttpResponseRedirect(reverse('card:history'))
