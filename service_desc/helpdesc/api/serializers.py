from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from ..models import Request


class RequestSerializer(ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    priority = serializers.CharField(source='get_priority_display')
    resolution = serializers.CharField(source='get_resolution_display')

    class Meta:
        model = Request
        fields = ['name', 'user', 'info', 'date_create', 'date_last_update','status','priority','resolution','flag_delete', 'flag_reopen']
