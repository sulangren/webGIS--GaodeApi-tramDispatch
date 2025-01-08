# models.py
from django.contrib.gis.db import models

# 用户表
class User(models.Model):
    class Meta():
        db_table = 'db_user'
    # 用户名
    username = models.CharField(max_length=15, unique=True,null=False)
    # 密码
    password = models.CharField(max_length=15,null=False)
    # 电话号码
    telephone = models.CharField(max_length=12,unique=True,null=True)


class staffUser(models.Model):
    class Meta():
        db_table = 'db_staff_user'

    # 用户名
    staff_username = models.CharField(max_length=15, unique=True, null=False)
    # 密码
    staff_password = models.CharField(max_length=15, null=False)
    # 电话号码
    staff_telephone = models.CharField(max_length=12, unique=True,null=True)


# 停车区域表
class ParkingArea(models.Model):
    class Meta():
        db_table = 'db_parking_area'

    # 划分的区域
    area_id = models.IntegerField(null=False)
    # 区域名称
    area_name = models.CharField(max_length=20, null=False)
    # 停车面数据
    parking_area = models.GeometryField(dim=2, null=False)
    # 停车场中心坐标
    polygon_center = models.PointField(null=False)
    # 停车场负责人
    # manage_parking_area=models.ForeignKey(staffUser,null=True,on_delete=models.CASCADE)


# 车辆数据表
class Bicycle(models.Model):
    class Meta():
        db_table = 'db_bicycle'

    # 自行车状态
    status = models.CharField(max_length=3,default='正常')
    # 当前所属停车点位置
    current_location = models.ForeignKey(ParkingArea, on_delete=models.CASCADE, null=False)
    # 车辆当前位置
    coordinates = models.PointField(null=False)  # 点数据
    # 车辆当前剩余电量
    remaining_battery = models.FloatField()


class Dispatch(models.Model):
    class Meta():
        db_table = 'db_dispatch'

    # 调度的自行车
    bicycle = models.OneToOneField(Bicycle, on_delete=models.CASCADE)
    # 调度起始停车点
    start_parking_area = models.ForeignKey(ParkingArea, on_delete=models.CASCADE, related_name='start_area')
    # 调度结束停车点
    end_parking_area = models.ForeignKey(ParkingArea, on_delete=models.CASCADE, related_name='end_area')
    # 调度起始时间
    dispatch_time = models.DateTimeField()
    # 调度结束时间
    completion_time = models.DateTimeField()
    # 调度负责人
    # dispatch_uers=models.ForeignKey(staffUser,null=True,on_delete=models.CASCADE)


# 日期表模型，用于记录每日停车点内车的数量
class DailyParkingStats(models.Model):
    # 创建复合唯一约束，确保每天一个区域只有一个记录
    class Meta:
        unique_together = ('date', 'parking_area')
        db_table = 'db_daily_parking_stats'

    # 日期，使用DateField存储
    date = models.DateField(null=False)
    # 外键关联 ParkingArea 表
    parking_area = models.ForeignKey(ParkingArea, related_name='daily_stats', on_delete=models.CASCADE)
    # 当日停车点内的车的数量
    vehicle_count = models.IntegerField(null=False)

