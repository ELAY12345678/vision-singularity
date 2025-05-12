from rest_framework import serializers
from .models import Table, ServiceCall, Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Restaurant
        fields = '__all__'

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Table
        fields = '__all__'

class ServiceCallSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ServiceCall
        fields = '__all__'


