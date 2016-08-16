from __future__ import absolute_import

from django.conf.urls import patterns, include, url

from sentry.plugins import plugins


urlpatterns = patterns('')

for _plugin in plugins.all():
    _plugin_group_urls = _plugin.get_group_urls()
    if _plugin_group_urls:
        urlpatterns.append(
            url(r'^%s/' % _plugin.slug, include(patterns('', _plugin_group_urls)))
        )
