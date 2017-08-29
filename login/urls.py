from django.conf.urls import url

from login import views

urlpatterns = [
    url(r'^login/$', views.loginpage, name="loginpage"),
    url(r'^login/userin/$', views.userin, name="userin"),#ajax
    url(r'^login/adduser/$', views.adduser, name="adduser"),#ajax
    url(r'^logout/$', views.userout, name="userout")
]
