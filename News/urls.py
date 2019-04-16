from django.conf.urls import url

from News import api

urlpatterns = [
    url(r'^get_swiper/',api.get_swiper),
    url(r'^push_news/',api.push_news),
    url(r'^new_lists/', api.new_lists),
    url(r'^new_detail/', api.new_detail),
]
