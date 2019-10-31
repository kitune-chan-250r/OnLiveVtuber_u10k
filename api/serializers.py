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
    uid_serializer = serializers.PrimaryKeyRelatedField(queryset=Vtuber.objects.all(), write_only=True)
    uid = VtuberSerializer(read_only=True)
    class Meta:
        model = On_Live
        fields = ('uid', 'start_time', 'live_title', 'live_url', 'uid_serializer')

    def create(self, validated_data):
        validated_data['uid'] = validated_data.get('uid_serializer', None)
        if validated_data['uid'] is None:
            raise serializers.ValidationError("error vtuber not found")
        del validated_data['uid_serializer']

        return On_Live.objects.create(**validated_data)