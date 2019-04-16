from django.conf.urls import url

from Back import api

urlpatterns = [
    url(r'^get_news/',api.get_news),
    url(r'^login/',api.login),
    url(r'^auther/',api.auther),
    url(r'^auther_sort/',api.auther_sort),
    url(r'^append_auther/',api.append_auther),
    url(r'^confirm_auther/',api.confirm_auther),
    url(r'^modify_auther/',api.modify_auther),
    url(r'^search_auther/',api.search_auther),
    url(r'^remove_auther/',api.remove_auther),
    url(r'^news/',api.news),
    url(r'^append_new/',api.append_new),
    url(r'^modify_new/',api.modify_new),
    url(r'^confirm_new/',api.confirm_new),
    url(r'^search_new/',api.search_new),
    url(r'^news_sort/',api.news_sort),
    url(r'^remove_new/',api.remove_new),
    url(r'^logout/',api.logout),
]
