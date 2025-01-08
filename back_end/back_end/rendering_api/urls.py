# urls.py

from django.contrib import admin
from django.urls import path, include

from rendering_api.views import QuerySortedListView, QueryBicycleListView

urlpatterns = [
    path('default/', QuerySortedListView.as_view(), name='rendering-default'),
    path('point/', QueryBicycleListView.as_view(), name='rendering-point'),
]
