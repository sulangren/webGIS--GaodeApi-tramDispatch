# serializers.py
from rest_framework import serializers
from enroll.models import ParkingArea,Bicycle
from django.db import models

class ParkingAreaSerializer(serializers.ModelSerializer):
    coordinates = serializers.SerializerMethodField()

    class Meta:
        model = ParkingArea
        fields = ['coordinates']  # 只返回 coordinates

    def get_coordinates(self, obj):
        # 获取停车区域的坐标
        if obj.parking_area:
            # 提取坐标数据并返回为列表（嵌套数组）
            coords = obj.parking_area.coords
            # 将坐标从元组转换为列表，并返回
            return [list(coord) for coord in coords[0]]  # 转换为嵌套的列表
        return []

class BicycleSerializer(serializers.ModelSerializer):
    coordinates = serializers.SerializerMethodField()

    class Meta:
        model = Bicycle
        fields = ['id', 'coordinates']  # 只返回id和coordinates

    def get_coordinates(self, obj):
        # 获取自行车坐标
        print([obj.coordinates.x, obj.coordinates.y])
        return [obj.coordinates.x, obj.coordinates.y]  # 将坐标转换为列表



