from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('vtuber', vtuber, name='vtuber'),
    path('request', request_page, name='request'),
]
