from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.utils import timezone
from ..models import Project, Work, User


def create(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    # user = 2 until login implemented
    project.work_set.create(user_id=2, start_time=timezone.now())
    return HttpResponseRedirect(reverse('card:index'))
