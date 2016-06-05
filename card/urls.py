from django.conf.urls import url

from . import views

app_name = "card"
urlpatterns = [
    url(r'^$', views.home.index, name='index'),

    url(r'^project/$', views.project.index, name='project'),
    url(r'^project/new/$', views.project.create, name='new_project'),
    url(r'^(?P<project_id>[0-9]+)/project/$', views.project.show, name='view_project'),
    url(r'^(?P<project_id>[0-9]+)/project/delete$', views.project.destroy, name='destroy_project'),
    url(r'^(?P<project_id>[0-9]+)/project/complete$', views.project.complete, name='complete_project'),

    url(r'^(?P<project_id>[0-9]+)/work/new/$', views.work.create, name='new_work'),
    url(r'^(?P<work_id>[0-9]+)/work/done/$', views.work.done, name='work_done'),
    url(r'^work/add/$', views.work.add, name='add_work'),
    url(r'^work/add/new$', views.work.add_new_work, name='add_new_work'),

    url(r'^balance/$', views.balance.index, name='balance'),

    url(r'^history/$', views.history.index, name='history'),

    url(r'^login+$', views.user.login_show, name='login_show'),
    url(r'^login/user/$', views.user.login_user, name='login'),
    url(r'^register/$', views.user.register_show, name='register_show'),
    url(r'^register/user/$', views.user.register_user, name='register'),
    url(r'^logout/$', views.user.logout_user, name='logout'),
    url(r'^settings/$', views.user.settings, name='settings'),
    url(r'^settings/change/$', views.user.change_settings, name='change_settings'),
]
