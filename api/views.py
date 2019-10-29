from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Vtuber, On_Live
from .serializers import *

# Create your views here.

class VtuberViewSet(viewsets.ModelViewSet):
    queryset = Vtuber.objects.all()
    serializer_class = VtuberSerializer


class OnLiveViewSet(viewsets.ModelViewSet):
    queryset = On_Live.objects.all()
    serializer_class = OnLiveSerializer