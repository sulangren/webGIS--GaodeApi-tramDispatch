from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from enroll.models import Bicycle, ParkingArea
from function_api.serializers import BufferSerializer, CenterPointSerializer

from algorithm import getDistanceData,getDemandData,scheduling,optimization


class FiftyGenerateBufferView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        """
        接收 POST 请求，根据指定 ID 获取坐标，构建缓冲区（半径为 50 米），并返回缓冲区内的自行车数据。
        """
        # 获取请求体中的数据（传递的是单一的自行车 ID）
        bike_id = request.data.get("id")  # 获取请求中的自行车 ID

        if not bike_id:
            return Response({"code": 1, "message": "No bicycle ID provided"}, status=status.HTTP_400_BAD_REQUEST)

        # 根据 ID 查询自行车信息
        try:
            bicycle = Bicycle.objects.get(id=bike_id)
        except Bicycle.DoesNotExist:
            return Response({"code": 1, "message": "Bicycle not found for the provided ID"}, status=status.HTTP_404_NOT_FOUND)

        # 获取当前自行车的坐标
        bike_point = bicycle.coordinates

        # 将坐标从 EPSG:4326 转换为 EPSG:3857 坐标系
        bike_point_3857 = bike_point.transform(3857, clone=True)

        # 创建 50 米的缓冲区（单位为米）
        buffer = bike_point_3857.buffer(60)  # 50 米的缓冲区

        # 将缓冲区从 EPSG:3857 转换回 EPSG:4326 坐标系
        buffer_4326 = buffer.transform(4326, clone=True)

        # 查找在该缓冲区内的所有自行车（排除当前自行车）
        bicycles_in_buffer = Bicycle.objects.filter(coordinates__within=buffer_4326).exclude(id=bike_id)

        # 将在缓冲区内的自行车数据格式化返回
        bicycles_within_buffer = BufferSerializer(bicycles_in_buffer, many=True).data

        # 返回结果
        result = {
            "code": 0,
            "data": [
                # 当前自行车数据
                {
                    "id": bicycle.id,
                    "coordinates": [bike_point.x, bike_point.y]  # 当前自行车的坐标
                },
                # 缓冲区内的其他自行车数据
                *bicycles_within_buffer
            ]
        }
        print(result)
        return Response(result)


# 100米缓冲区
class HundredGenerateBufferView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        """
        接收 POST 请求，根据指定 ID 获取坐标，构建缓冲区（半径为 100 米），并返回缓冲区内的自行车数据。
        """
        # 获取请求体中的数据（传递的是单一的自行车 ID）
        bike_id = request.data.get("id")  # 获取请求中的自行车 ID
        print(bike_id)

        if not bike_id:
            return Response({"code": 1, "message": "No bicycle ID provided"}, status=status.HTTP_400_BAD_REQUEST)

        # 根据 ID 查询自行车信息
        try:
            bicycle = Bicycle.objects.get(id=bike_id)
        except Bicycle.DoesNotExist:
            return Response({"code": 1, "message": "Bicycle not found for the provided ID"}, status=status.HTTP_404_NOT_FOUND)

        # 获取当前自行车的坐标
        bike_point = bicycle.coordinates

        # 创建 100 米的缓冲区
        buffer = bike_point.buffer(100)  # 半径 100 米

        # 查找在该缓冲区内的所有自行车（排除当前自行车）
        bicycles_in_buffer = Bicycle.objects.filter(coordinates__within=buffer).exclude(id=bike_id)

        # 将在缓冲区内的自行车数据格式化返回
        bicycles_within_buffer = BufferSerializer(bicycles_in_buffer, many=True).data

        # 返回结果
        result = {
            "code": 0,
            "data": [
                # 当前自行车数据
                {
                    "id": bicycle.id,
                    "coordinates": [bike_point.x, bike_point.y]  # 当前自行车的坐标
                },
                # 缓冲区内的其他自行车数据
                *bicycles_within_buffer
            ]
        }
        return Response(result)

class CenterPointListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        # 获取所有区域的中心点，并格式化
        query = ParkingArea.objects.all()
        serializer = CenterPointSerializer(query, many=True)
        print(f'{serializer.data}')


        return Response({
            'code': 0,
            'data': serializer.data  # 返回包含id和coordinates的列表
        })


class RouteCalculationResultView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        # 获取所有停车区信息
        query = ParkingArea.objects.all()
        area_dict = {area.id: {
            'area_name': area.area_name,
            'polygon_center': [area.polygon_center.x, area.polygon_center.y]
        } for area in query}

        # 模拟从Excel文件中获取的距离矩阵数据
        distances_data = ''
        distances = getDistanceData.GetDistanceData(distances_data)

        # 模拟从Excel文件中获取的需求量数据
        distances_data_one = ''
        distances_data_tow = ''
        initial_demand = getDemandData.GetDemandData(distances_data_one, distances_data_tow)

        # 获取前端传递的搬运车量容量
        bike_capacity = request.data.get("capacity")
        if bike_capacity is None:
            return Response({"error": "Capacity value is required"}, status=400)  # 如果没有传递容量值，返回错误
        bike_capacity = int(bike_capacity)  # 转换为整数

        # 创建调度器对象
        scheduler = scheduling.VehicleScheduler(
            distances.get_distance_data(),
            bike_capacity,
            initial_demand.HelpData(),
        )

        # 调度
        scheduler.schedule()

        # 处理调度结果
        processor = optimization.VehicleSchedulerResultProcessor(
            scheduler,
            fixed_threshold_small=4,
            fixed_threshold_large=5,
            large_threshold=30
        )
        processed_routes = processor.process_routes()

        # 处理调度结果并扁平化
        final_routes = []
        for route in processed_routes:
            from_area_id = route['from']
            to_area_id = route['to']

            from_info = area_dict.get(from_area_id, {})
            to_info = area_dict.get(to_area_id, {})

            final_route = {
                'dispatch_count': route['dispatch_count'],
                'from': from_info.get('area_name', 'Unknown'),
                'fromPoint': from_info.get('polygon_center', [None, None]),
                'to': to_info.get('area_name', 'Unknown'),
                'toPoint': to_info.get('polygon_center', [None, None]),
                'path': route['path'],
                'transfer_amount': route['transfer_amount']
            }

            final_routes.append(final_route)

        # 返回数据
        return Response({
            'code': 0,
            'data': final_routes  # 返回的 data 是一个平坦的列表
        })

    def get(self, request, format=None):
        return Response({
            'code': 0,
        })