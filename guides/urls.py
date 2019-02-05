from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name="guides.views.index"),
    url(r'matcher$', views.matcher_index, name="guides.views.matcher_index"),
    url(r'become_guide$', views.become_guide, name='guides.views.become_guide'),
    url(r'request_guide$', views.request_guide, name='guides.views.request_guide'),
    url(r'edit_info/(?P<hash>[\w]+)$', views.edit_info, name='guides.views.edit_info'),
    url(r'make_match$', views.make_match, name='guides.views.make_match'),
    url(r'send_match_email/(?P<match_id>[\d]+)$', views.send_match_email, name='guides.views.send_match_email')
]
