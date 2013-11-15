from django.conf.urls import *
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url('^$', TemplateView.as_view(template_name="ospi/home.html")),
    url('^zones/$', TemplateView.as_view(template_name="ospi/zones.html")),
    url('^schedule/$', TemplateView.as_view(template_name="ospi/schedule.html")),
    url('^settings/$', TemplateView.as_view(template_name="ospi/settings.html")),
)
