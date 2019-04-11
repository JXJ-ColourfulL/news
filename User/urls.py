from django.conf.urls import url

from User import api

urlpatterns = [
    url(r'^get_user/',api.get_user),
    url(r'^login/',api.login),
    url(r'^register/',api.register),
    url(r'^logout/',api.logout),
    url(r'^update_avatar/',api.update_avatar),
]