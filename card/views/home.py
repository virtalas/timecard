from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.utils import timezone
from ..models import Project, Work, User


def index(request):
    projects = Project.objects.order_by('-name')
    context = {
        'projects': projects
    }
    return render(request, 'card/index.html', context)
