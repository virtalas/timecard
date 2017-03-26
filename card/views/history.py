from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from datetime import date
import time
from django.utils import timezone
from ..models import Project, Work, Minutes

from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required(login_url='/timecard/login')
def index(request):
    user_id = request.user.id
    work_all = Work.objects.order_by('-start_time').filter(user_id=user_id)
    paginator = Paginator(work_all, 17)

    page = request.GET.get('page')
    try:
        work = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        work = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        work = paginator.page(paginator.num_pages)

    context = {
        "work_list": work,
        "page_number_range": range(1, paginator.num_pages + 1)
    }

    return render(request, 'card/history/index.html', context)
