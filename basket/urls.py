from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^basket/$', views.basket_page, name="basket_page"),
    url(r'^basket/remove/$', views.basket_remove, name="basket_remove"),#ajax
    url(r'^basket/number/$', views.basket_number, name="basket_number"),#ajax
    url(r'^basket/add/$', views.basket_add, name="basket_add"),#ajax
]
