from algorithm import getDistanceData, getDemandData, scheduling

class VehicleSchedulerResultProcessor:
    def __init__(self, scheduler, fixed_threshold_small=4, fixed_threshold_large=5, large_threshold=30):
        """
        处理调度结果
        :param scheduler: 原始调度器对象
        :param fixed_threshold_small: 承载量小于30时的固定阈值（小于此值的调度将被排除）
        :param fixed_threshold_large: 承载量大于等于30时的固定阈值（小于此值的调度将被排除）
        :param large_threshold: 承载量超过此值时，使用固定阈值
        """
        self.scheduler = scheduler  # 调度器对象
        self.fixed_threshold_small = fixed_threshold_small  # 承载量小于30时的固定阈值
        self.fixed_threshold_large = fixed_threshold_large  # 承载量大于等于30时的固定阈值
        self.large_threshold = large_threshold  # 承载量大于此值时使用固定阈值

    def process_routes(self):
        """
        处理调度结果，根据承载量和阈值条件过滤调度
        """
        # 过滤调度项
        filtered_routes = []

        for route in self.scheduler.routes:
            transfer_amount = route['transfer_amount']

            # 根据承载量和运输量进行过滤
            if self.scheduler.capacities < self.large_threshold and transfer_amount < self.fixed_threshold_small:
                # 如果承载量小于30且运输量小于4，则排除此调度项
                continue
            if self.scheduler.capacities >= self.large_threshold and transfer_amount < self.fixed_threshold_large:
                # 如果承载量大于等于30且运输量小于5，则排除此调度项
                continue

            # 将符合条件的调度项加入filtered_routes
            filtered_routes.append(route)

        # 重新排序调度次数
        for i, route in enumerate(filtered_routes):
            route['dispatch_count'] = i + 1  # 更新dispatch_count，从1开始排序

        # 更新调度器的 routes
        self.scheduler.routes = filtered_routes

        # 打印处理后的结果
        print("Processed Routes:")
        for route in self.scheduler.routes:
            print(f"Dispatch #{route['dispatch_count']}: Transporting {route['transfer_amount']} vehicles from {route['from']} to {route['to']} along path {route['path']}")

        return self.scheduler.routes


# # 创建调度器对象
# capacities = 5  # 可根据需要修改此值
# distances_data = '../Excel/distanceWeightMatrix.xlsx'
# distances = getDistanceData.GetDistanceData(distances_data)
#
# # 每个站点的初始需求量，正值多车，负值少车
# distances_data_one = '../Excel/onHand.xlsx'
# distances_data_tow = '../Excel/baseValue.xlsx'
# initial_demand = getDemandData.GetDemandData(distances_data_one,distances_data_tow)
#
# scheduler = scheduling.VehicleScheduler(distances.get_distance_data(), capacities, initial_demand.HelpData(), threshold_percentage=0.2)
#
# # 调度
# scheduler.schedule()
#
# # 处理调度结果
# processor = VehicleSchedulerResultProcessor(scheduler, fixed_threshold_small=4, fixed_threshold_large=5, large_threshold=30)
# processed_routes = processor.process_routes()
#
# # 输出最终处理结果
# print("Final Processed Routes: ", processed_routes)
