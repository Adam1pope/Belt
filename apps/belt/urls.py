from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
  url(r'^$', views.index),
  url(r'^register', views.register),
  url(r'^appointments', views.appointments),
  url(r'^login', views.login),
  url(r'^process', views.process),
  url(r'^edit', views.edit),
  url(r'^delete', views.delete),
  url(r'^update', views.update),

]