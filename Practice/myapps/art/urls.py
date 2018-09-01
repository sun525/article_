from django.conf.urls import url
from art import views

urlpatterns = [
    url(r'^show/(\d+?)/', views.show),
    url(r'^search/$', views.search, name='search'),
    url(r'^detail/(\d+?)/', views.detail, name='detail'),
    url(r'^qd/(\d+?)/', views.qdArt),
    url(r'^query_qd/(\d+?)/', views.queryQDState),
]