# 总路由
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('enroll.urls')),
    path("query/", include('query_api.urls')),
    path("rendering/", include('rendering_api.urls')),
    path("function/", include('function_api.urls')),
]
