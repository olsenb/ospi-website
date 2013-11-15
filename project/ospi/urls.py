from django.conf.urls import *
from .views import *
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url('^$', TemplateView.as_view(template_name="ospi/home.html")),
    url('^zones/$', TemplateView.as_view(template_name="ospi/zones.html")),
    url('^zones/create/$', CreateZoneView.as_view(), name="zone_create"),
    url('^schedule/$', TemplateView.as_view(template_name="ospi/schedule.html"), name="schedule_list"),
    url('^schedule/create/$', CreateScheduleView.as_view(), name='schedule_create'),
    url('^settings/$', TemplateView.as_view(template_name="ospi/settings.html")),
)
