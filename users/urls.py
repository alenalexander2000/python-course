from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^signin/process/$', views.loginprocess),
    url(r'^signup/process/$', views.signupprocess),

    url(r'^signin/$', views.signin_page),

    # exception page
    url(r'^', views.signup_page),
]
