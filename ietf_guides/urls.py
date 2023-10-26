from django.urls import include, re_path
from django.contrib import admin

from guides.views import index as guides_index

urlpatterns = [
    re_path(r'^$', guides_index),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    re_path(r'^guides/', include('guides.urls')),
]
