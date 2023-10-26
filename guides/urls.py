from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.index, name="guides.views.index"),
    re_path(r'matcher$', views.matcher_index, name="guides.views.matcher_index"),
    re_path(r'become_guide$', views.become_guide, name='guides.views.become_guide'),
    re_path(r'request_guide$', views.request_guide, name='guides.views.request_guide'),
    re_path(r'edit_info/(?P<hash>[\w]+)$', views.edit_info, name='guides.views.edit_info'),
    re_path(r'make_match$', views.make_match, name='guides.views.make_match'),
    re_path(r'send_match_email/(?P<match_id>[\d]+)$', views.send_match_email, name='guides.views.send_match_email')
]
