from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^order/all/$', views.myorders, name="myorders"),
    url(r'^order/add/$', views.addorder, name="addorder"),#ajax
    url(r'^order/cancel/$', views.cancelorder, name="cancelorder"),#ajax
]