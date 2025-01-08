import heapq

from algorithm import getDistanceData,getDemandData

class VehicleScheduler:
    def __init__(self, distances, capacities, initial_demand):
        """
        初始化调度器
        :param distances: 二维矩阵，表示站点之间的距离
        :param capacities: 每次运输的最大承载量
        :param initial_demand: 每个站点的初始需求量（正值表示多车，负值表示少车）
        """
        self.distances = distances  # 站点之间的距离矩阵
        self.capacities = capacities  # 每次运输的最大承载量
        self.demand = initial_demand  # 每个站点的需求量，正值表示多车，负值表示少车
        self.num_nodes = len(distances)  # 站点数量
        self.routes = []  # 记录每次调度的路径
        self.schedule_count = 0  # 调度次数计数器

    def dijkstra(self, start):
        """
        Dijkstra 算法求最短路径
        :param start: 起始站点
        :return: 最短路径的距离数组和前驱节点数组
        """
        dist = [float('inf')] * self.num_nodes  # 距离数组
        dist[start] = 0  # 起始点到自身的距离为0
        pq = [(0, start)]  # 优先队列，存储当前节点及其距离
        prev = [-1] * self.num_nodes  # 记录最短路径的前驱节点

        while pq:
            d, node = heapq.heappop(pq)
            if d > dist[node]:
                continue

            for neighbor in range(self.num_nodes):
                if neighbor != node:
                    new_dist = d + self.distances[node][neighbor]
                    if new_dist < dist[neighbor]:
                        dist[neighbor] = new_dist
                        prev[neighbor] = node
                        heapq.heappush(pq, (new_dist, neighbor))

        return dist, prev

    def get_path(self, prev, end):
        """
        根据前驱节点数组还原路径
        :param prev: 前驱节点数组
        :param end: 终点
        :return: 路径
        """
        path = []
        while end != -1:
            path.append(end)
            end = prev[end]
        return path[::-1]  # 反转路径

    def adjust_demand(self, from_node, to_node, transfer_amount):
        """
        调整起始站点和目标站点的需求量
        :param from_node: 起始站点
        :param to_node: 目标站点
        :param transfer_amount: 每次调动的车辆数量
        """
        self.demand[from_node] -= transfer_amount  # 运输量减少
        self.demand[to_node] += transfer_amount    # 运输量增加

    def schedule(self):
        """
        主调度函数，迭代执行调度
        """
        while any(d != 0 for d in self.demand):  # 当存在需要调整的站点时
            # 找出需求量为正的站点（车多的地方）
            positive_nodes = [i for i, d in enumerate(self.demand) if d > 0]
            # 找出需求量为负的站点（车少的地方）
            negative_nodes = [i for i, d in enumerate(self.demand) if d < 0]

            # 如果没有车多或车少的地方，跳出
            if not positive_nodes or not negative_nodes:
                break

            # 遍历每个车多的站点
            for from_node in positive_nodes:
                if self.demand[from_node] == 0:
                    continue

                # 遍历每个车少的站点
                for to_node in negative_nodes:
                    if self.demand[to_node] == 0:
                        continue

                    # 计算每次调度的车辆数
                    transfer_amount = min(self.capacities, abs(self.demand[to_node]), self.demand[from_node])

                    if transfer_amount == 0:
                        continue

                    # 获取最短路径
                    dist, prev = self.dijkstra(from_node)
                    path = self.get_path(prev, to_node)

                    # 调整需求量
                    self.adjust_demand(from_node, to_node, transfer_amount)

                    # 调度次数递增
                    self.schedule_count += 1

                    # 记录调度的路径和调动的车辆数，包含调度次数
                    self.routes.append({
                        'dispatch_count': self.schedule_count,  # 添加调度次数
                        'from': from_node,
                        'to': to_node,
                        'path': path,
                        'transfer_amount': transfer_amount
                    })

                    # print(f"Dispatch #{self.schedule_count}: Transporting {transfer_amount} vehicles from {from_node} to {to_node} along path {path}")
                    break  # 每次调动一次，找到合适的路径后跳出

        # print("Scheduling complete!")
        print("Routes taken: ", self.routes)
        return self.routes


# # 每次运输的最大承载量
# capacities = 10
#
# # 数据
# distances_data = '../Excel/distanceWeightMatrix.xlsx'
# distances = getDistanceData.GetDistanceData(distances_data)
#
# # 每个站点的初始需求量，正值多车，负值少车
# distances_data_one = '../Excel/onHand.xlsx'
# distances_data_tow = '../Excel/baseValue.xlsx'
# initial_demand = getDemandData.GetDemandData(distances_data_one,distances_data_tow)
#
# # 创建调度器对象
# scheduler = VehicleScheduler(distances.get_distance_data(), capacities, initial_demand.HelpData())
#
# # 开始调度
# scheduler.schedule()
