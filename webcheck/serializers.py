from rest_framework import serializers
from .models import UrlCheck, Test


class CreateUrlCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlCheck
        fields = ['url']


class UrlCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlCheck
        fields = '__all__'
        read_only_fields = ('created_at', 'id')
