from django.conf.urls import url

from News import api

urlpatterns = [
    url(r'^get_news/',api.get_news),
]
