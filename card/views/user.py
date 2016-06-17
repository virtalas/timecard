from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

import datetime
from django.utils import timezone
from ..models import Project, Work, Minutes
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required


def login_show(request):
    return render(request, 'card/user/login.html')

def login_user(request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(username=email, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('card:index'))
    else:
        context = {
            'email': request.POST['email'],
            'error': "The email and password were incorrect."
        }
        return render(request, 'card/user/login.html', context)

def register_show(request):
    return render(request, 'card/user/register.html')

def register_user(request):
    name = request.POST['firstname']
    email = request.POST['email']
    password1 = request.POST['password']
    password2 = request.POST['password2']

    if password1 == password2:
        # Create user
        user = User.objects.create_user(first_name=name, username=email, email=email, password=password1)
        user_auth = authenticate(username=email, password=password1)
        login(request, user_auth)

        # Create minutes_per_day for this user
        minutes = Minutes(user_id=user.id, minutes_per_day=480, start_date=datetime.datetime.now().replace(hour=0, minute=0))
        minutes.save()

        return HttpResponseRedirect(reverse('card:index'))
    else:
        context = {
            'firstname': name,
            'username': username,
            'errors': ["Passwords didn't match."]
        }
        return render(request, 'card/user/register.html', context)

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('card:index'))

@login_required(login_url='/card/login')
def settings(request):
    user_id = request.user.id
    # minutes_per_day = Minutes.objects.minutes_per_day(user_id)
    # hours_per_day = Minutes.objects.hours_per_day(user_id)
    minutes = Minutes.objects.filter(user_id=user_id).order_by("-start_date")
    current_minutes_per_day = Minutes.objects.current_minutes_per_day(user_id)
    current_hours_per_day = Minutes.objects.current_hours_per_day(user_id)

    context = {
        'minutes': minutes,
        'current_minutes_per_day': current_minutes_per_day,
        'current_hours_per_day': current_hours_per_day,
        'full_hours': int(current_minutes_per_day / 60),
        'leftover_minutes': current_minutes_per_day % 60
    }

    return render(request, 'card/user/settings.html', context)

@login_required(login_url='/card/login')
def new_hours_per_day(request):
    user_id = request.user.id

    if not request.POST['end_date']:
        # User is changing the currently active hours per day
        end_date = None
        # Deal with the currently active one first
        current_m_list = Minutes.objects.filter(user_id=user_id, end_date__isnull=True)
        current_m = current_m_list[0]
        current_m.end_date = datetime.datetime.now().date()
        current_m.save()
    else:
        # User is adding an hours per day for a past time period
        end_date = request.POST['end_date']

    start_date = datetime.datetime.strptime(request.POST['start_date'], "%Y-%m-%d").date()
    hours = float(request.POST['hours'])
    minutes_per_day = int(hours * 60)

    m = Minutes(user_id=user_id, minutes_per_day=minutes_per_day, start_date=start_date, end_date=end_date)
    m.save()

    return HttpResponseRedirect(reverse('card:settings'))

@login_required(login_url='/card/login')
def edit_minutes(request, minutes_id):
    minutes = get_object_or_404(Minutes, pk=minutes_id)
    return render(request, 'card/user/edit_minutes.html', {"minutes": minutes})

@login_required(login_url='/card/login')
def update_minutes(request, minutes_id):
    return HttpResponseRedirect(reverse('card:settings'))
