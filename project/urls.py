from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url('^$', RedirectView.as_view(url="/ospi/"), name="home"),
    url('^ospi/', include('project.ospi.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
