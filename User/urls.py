from django.conf.urls import url

from User import api

urlpatterns = [
    url(r'^login/',api.login),
]