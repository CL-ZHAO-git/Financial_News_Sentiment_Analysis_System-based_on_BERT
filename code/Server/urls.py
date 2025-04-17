from django.conf.urls import url
from demo1 import views

urlpatterns = [
    url('', views.home),
    url('hello/', views.hello),
    url('form/', views.demo1_form)
    ]