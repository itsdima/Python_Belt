from django.conf.urls import url 
from . import views 

urlpatterns = [
	url(r'^main$', views.index),
	url(r'^travels$', views.travels), 
	url(r'^travels/destination/(?P<number>\d+)$', views.destination), 
	url(r'^travels/add$', views.add), 
	url(r'^processuser$', views.processuser), 
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
	url(r'^processadd$', views.processadd), 
	url(r'^jointrip/(?P<number>\d+)$', views.jointrip)

]