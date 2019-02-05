from django.conf.urls import include, url
from django.contrib import admin

from guides.views import index as guides_index

urlpatterns = [
    url(r'^$', guides_index),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^guides/', include('guides.urls')),
]
