from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Vtuber, On_Live
from .serializers import *
from django.db.models import Q #or検索

# Create your views here.

class VtuberViewSet(viewsets.ModelViewSet):
    queryset = Vtuber.objects.all()
    serializer_class = VtuberSerializer
    filter_fields = ('gender', 'uid')

    #検索
    def get_queryset(self):
        queryset = Vtuber.objects.all()
        search_query = self.request.query_params.get('search_query', None)
        if search_query is not None:
            queryset = queryset.filter(Q(liver_name__icontains=search_query) |
                                       Q(uid__icontains=search_query))
        return queryset


class OnLiveViewSet(viewsets.ModelViewSet):
    queryset = On_Live.objects.all()
    serializer_class = OnLiveSerializer
    filter_fields = ('uid',)

    def get_queryset(self):
        queryset = On_Live.objects.all()
        live_title = self.request.query_params.get('live_title', None)
        liver = self.request.query_params.get('liver', None)
        if live_title is not None:
            queryset = queryset.filter(live_title__icontains=live_title)
        if liver is not None:
            queryset = queryset.filter(uid__liver_name__icontains=liver)
        return queryset