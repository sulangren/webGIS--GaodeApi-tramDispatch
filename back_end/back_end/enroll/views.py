from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from enroll.serializers import CustomUserSerializer, UserLoginSerializer

from django.http import JsonResponse

def home(request):
    return HttpResponse("Welcome to the homepage.")

class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():  # 调用 is_valid() 以验证数据
            user = serializer.save()
            return Response({
                "code": 0,
                "data": {
                    "id": user.id,
                    "username": user.staff_username
                }
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)  # 输出序列化器的错误信息
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                'code': 0,
                'token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'data': user.username  # 返回 staff_username 或 username
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

