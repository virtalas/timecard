from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

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
        minutes = Minutes(user_id=user.id, minutes_per_day=480) # default 8h = 480min
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
    minutes_per_day = Minutes.objects.minutes_per_day(user_id)
    hours_per_day = Minutes.objects.hours_per_day(user_id)

    context = {
        'hours_per_day': hours_per_day,
        'minutes_per_day': minutes_per_day,
        'full_hours': int(minutes_per_day / 60),
        'leftover_minutes': minutes_per_day % 60
    }

    return render(request, 'card/user/settings.html', context)

@login_required(login_url='/card/login')
def change_settings(request):
    hours_per_day = float(request.POST['hours_per_day'])
    minutes = Minutes.objects.filter(user_id=request.user.id)
    m = minutes[0]
    m.minutes_per_day = int(hours_per_day * 60)
    m.save()

    return HttpResponseRedirect(reverse('card:settings'))
