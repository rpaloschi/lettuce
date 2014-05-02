from urllib.request import urlopen

from django.http import HttpResponse

from lettuce import step
from lettuce.django import django_url

from nose.tools import assert_equals

@step('I change the view code')
def change_view(step):
    from leaves import views
    def replacement(request):
        return HttpResponse('Changed')
    views.index = replacement

@step('The root page says "(.*)"')
def root_page_text(step, text):
    url = django_url('/')
    url = url.replace('0.0.0.0', '127.0.0.1')
    response = urlopen(url).read()
    assert_equals(str(response, encoding='UTF-8'), text)
