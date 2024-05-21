from rest_framework import serializers
from my_app.models import Category, CategoryRegion, Auto, Parking


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']


class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        fields = ['id', 'parking_count', 'is_active']


class CategoryRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryRegion
        fields = ['id', 'region', 'car_count', 'category']


class AutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auto
        fields = ['id', 'car_name', 'parking_number', 'car_id', 'car_qr', 'is_active', 'lat', 'long', 'created_at',
                  'category']
