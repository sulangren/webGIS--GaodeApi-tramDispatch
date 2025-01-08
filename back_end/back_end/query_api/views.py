 # vivew.py
from django.db.models import F
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from enroll.models import Bicycle
from .serializers import QuerySerializer
from rest_framework.permissions import AllowAny


# 商店排序列表视图
class QuerySortedListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        query = Bicycle.objects.all().order_by('-id')  # 直接使用 order_by 进行排序
        serializer = QuerySerializer(query, many=True)
        print()
        return Response({'code': 0, 'data': serializer.data})


class QuerySearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        queryset = Bicycle.objects.all()
        condition = request.query_params.get('selectedOption', None)
        if condition is not None:
            if condition == 'normal':
                queryset = queryset.filter(status__icontains='正常')
            elif condition == 'Low_battery':
                queryset = queryset.filter(remaining_battery__lte=20)
            elif condition == 'maintenance':
                queryset = queryset.filter(status__icontains='维护')
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        if not queryset.exists():
            return Response({'code': 1, 'message': 'No data found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = QuerySerializer(queryset, many=True)
        print(f"查询成功，查询的数据为：{serializer.data}")
        return Response({'code': 0, 'data': serializer.data})
