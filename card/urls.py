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

    url(r'^balance/$', views.balance.index, name='balance'),
]
