# serializers.py

from rest_framework import serializers
from enroll.models import Bicycle, ParkingArea
import pandas as pd


class BufferSerializer(serializers.ModelSerializer):
    coordinates = serializers.SerializerMethodField()

    class Meta:
        model = Bicycle
        fields = ['id', 'coordinates']  # 只返回 id 和 coordinates

    def get_coordinates(self, obj):
        # 获取自行车坐标
        return [obj.coordinates.x, obj.coordinates.y]  # 返回坐标 [x, y]

class CenterPointSerializer(serializers.ModelSerializer):
    polygon_center = serializers.SerializerMethodField()

    class Meta:
        model = ParkingArea
        fields = ['id', 'polygon_center', 'area_name']

    def get_polygon_center(self, obj):
        # 获取停车区域的中心坐标
        return [obj.polygon_center.x, obj.polygon_center.y]


