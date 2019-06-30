from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^signin/$', views.signin_page),

    #exception page
    url(r'^', views.signup_page),
]
