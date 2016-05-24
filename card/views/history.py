from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from datetime import date
import time
from django.utils import timezone
from ..models import Project, Work, User

from django.contrib.auth.decorators import login_required


@login_required(login_url='/card/login')
def index(request):
    context = {
    }

    return render(request, 'card/history/index.html', context)
