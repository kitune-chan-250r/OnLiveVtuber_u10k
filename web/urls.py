from django.urls import path, include
from django.views.generic import RedirectView
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('vtuber', vtuber, name='vtuber'),
    path('request', request_page, name='request'),
    path('reqmanag', request_manager),
    path('accept', accept_req, name='accept'),
    path('deny', deny_req, name='deny'),
    path(r'^favicon\.ico$',RedirectView.as_view(url='/static/images/favicon.ico')),
]
