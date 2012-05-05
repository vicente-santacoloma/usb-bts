from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^sign_up$', 'polls.views.sign_up'),
)
