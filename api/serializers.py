from rest_framework import serializers
from .models import Vtuber, On_Live, Request_vtuber

class VtuberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vtuber
        fields = ('uid', 'liver_name', 'gender', 'src')


class OnLiveSerializer(serializers.ModelSerializer):
    uid = VtuberSerializer()
    class Meta:
        model = On_Live
        fields = ('uid', 'start_time', 'live_title', 'live_url')

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request_vtuber
        fields = ('uid', 'liver_name', 'gender', 'twitter_id', 'src')

#uidのみでPOSTするためのシリアライザ
class OnLive_POST_Serializer(serializers.ModelSerializer):
    uid = serializers.PrimaryKeyRelatedField(queryset=Vtuber.objects.all())
    class Meta:
        model = On_Live
        fields = ('uid', 'start_time', 'live_title', 'live_url')