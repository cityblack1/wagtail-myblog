from .views import comment_view, contact_view

from django.conf.urls import include, url


urlpatterns = [
    url(r'^contact/$',contact_view , name='contact_me'),
    url(r'^(?P<slug>.*?)/$', comment_view, name='blog_comment'),
]
