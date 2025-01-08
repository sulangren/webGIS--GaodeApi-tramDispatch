# views.py
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from enroll.models import ParkingArea, Bicycle
from rendering_api.serializers import ParkingAreaSerializer,BicycleSerializer


class QuerySortedListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        # 获取所有停车区域数据，并按需要排序
        query = ParkingArea.objects.all()

        # 使用序列化器格式化数据
        serializer = ParkingAreaSerializer(query, many=True)

        # print(serializer.data)
        # 返回数据给前端，确保返回的 data 是数组
        return Response({
            'code': 0,
            'data': serializer.data  # 确保返回的 data 是数组
        })

class QueryBicycleListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        # 获取所有自行车数据，并格式化
        query = Bicycle.objects.all()
        serializer = BicycleSerializer(query, many=True)
        print(f'{serializer.data}')


        return Response({
            'code': 0,
            'data': serializer.data  # 返回包含id和coordinates的列表
        })
