from django.conf.urls import url, patterns

urlpatterns = patterns('',
    url(r'^rucola/$', 'first.views.rucola'),
    url(r'^tasty_rucola/$', 'second.views.tasty_rucola'),
)
