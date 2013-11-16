from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

# urlpatterns = patterns('keen.views',
#     url(r'^$', 'index'),
#
#     # Uncomment the admin/doc line below to enable admin documentation:
#     # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
#
#     # Uncomment the next line to enable the admin:
#     # url(r'^admin/', include(admin.site.urls)),
# )

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^$', TemplateView.as_view(template_name='index.html')),
    (r'^legal$', TemplateView.as_view(template_name='legal.html')),
)

#mdo special case
urlpatterns += patterns('main.views.customers',
    url(r'^mdo/signup/$', 'mdo_signup'),
)


#mdo special case
urlpatterns += patterns('main.views.clients',
    url(r'^handlebar/redeem/(?P<promo_code>[0-9A-Za-z]+)/$', 'handlebar_redeem'),
    url(r'^handlebar/redeem/$', 'handlebar_redeem'),
)
