from django.conf.urls import url

from User import api

urlpatterns = [
    url(r'^get_user_info/',api.get_user_info),
    url(r'^login/',api.login),
    url(r'^register/',api.register),
    url(r'^logout/',api.logout),
]