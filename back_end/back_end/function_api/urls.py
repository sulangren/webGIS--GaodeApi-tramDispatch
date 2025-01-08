# urls.py

from django.contrib import admin
from django.urls import path, include

from function_api.views import FiftyGenerateBufferView, CenterPointListView, RouteCalculationResultView

urlpatterns = [
    path('buffer/', FiftyGenerateBufferView.as_view(), name='function-buffer'),
    path('centerPoint/', CenterPointListView.as_view(), name='function-centerPoint'),
    path('pathPlanning/', RouteCalculationResultView.as_view(), name='function-pathPlanning'),
]
