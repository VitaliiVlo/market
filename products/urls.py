from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^category/(?P<category_id>[0-9]+)/$', views.category_page, name="category_page"),
    url(r'^category/(?P<category_id>[0-9]+)/product_filters/$', views.product_filters, name="product_filters"),  # ajax
    url(r'^product/(?P<product_id>[0-9]+)/$', views.product_page, name="product_page"),
    url(r'^product/add/comment/$', views.add_comment, name="add_comment"),  # ajax
]
