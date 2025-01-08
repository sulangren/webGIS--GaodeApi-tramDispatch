import pandas as pd


class GetDistanceData:
    def __init__(self, distance_data):
        self.distance_data = distance_data

    def get_distance_data(self):
        distance_datas = pd.read_excel(self.distance_data, sheet_name=0)
        # 将 distance_datas 转换为二维列表
        distance_datas = distance_datas.values.tolist()

        return distance_datas


