from django.conf.urls import include, url
from accounts import views
# from django.contrib import admin

urlpatterns = [
    url(r'^sand_email$', views.send_login_email, name='send_login_email'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout')
]
