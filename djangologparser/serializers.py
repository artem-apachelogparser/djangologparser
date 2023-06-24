from rest_framework import serializers
from .models import ApacheLog


class ApacheLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApacheLog
        fields = ['id', 'host', 'user_name', 'time', 'request', 'status', 'size', 'referer', 'user_agent']
