# serializers.py
from rest_framework import serializers
from enroll.models import Bicycle, ParkingArea

# 定义一个 ParkingArea 的序列化器
class ParkingAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingArea
        fields = ['area_name']  # 仅返回 area_name 字段

class QuerySerializer(serializers.ModelSerializer):
    # 将 current_location 字段转换为字符串（area_name）
    current_location = serializers.CharField(source='current_location.area_name')

    class Meta:
        model = Bicycle
        fields = ['id', 'status', 'current_location', 'remaining_battery']