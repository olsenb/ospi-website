from django.conf.urls import *
from .views import *
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url('^$', TemplateView.as_view(template_name="ospi/rpi_home.html"), name='rpi_home'),
    url('^stations/$', StationsListView.as_view(), name='stations_list'),
    url('^stations/create/$', CreateStationsView.as_view(), name="stations_create"),
    url('^stations/edit/(?P<pk>\d+)/$', UpdateStationsView.as_view(), name='stations_edit'),
    url('^schedule/$', ScheduleListView.as_view(), name="schedule_list"),
    url('^schedule/create/$', CreateScheduleView.as_view(), name='schedule_create'),
    url(
        '^stats/$',
        TemplateView.as_view(template_name="ospi/rpi_stats.html"),
        name="rpi_stats"
    ),
    url(
        '^logs/$',
        WaterLogView.as_view(),
        name="rpi_logs"
    ),
    url(
        '^settings/$',
        TemplateView.as_view(template_name="ospi/rpi_settings.html"),
        name="rpi_settings"
    ),
    url('^account/create/$', CreateAccountView.as_view(), name='account_create'),
)
