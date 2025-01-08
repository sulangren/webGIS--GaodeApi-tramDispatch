import pandas as pd


class GetDemandData:

    def __init__(self, on_hand, base_value):
        # 初始化时指定 Excel 文件路径
        self.on_hand = on_hand
        self.base_value = base_value


    def HelpData(self):
        # 读取 Excel 文件
        on_hand_data = pd.read_excel(self.on_hand, sheet_name=0)
        base_value_data = pd.read_excel(self.base_value, sheet_name=0)

        # 确保两者列完全对齐，只保留相同的列
        common_columns = on_hand_data.columns.intersection(base_value_data.columns)
        on_hand_data = on_hand_data[common_columns]
        base_value_data = base_value_data[common_columns]

        # 将所有列的数据类型转换为整数类型，避免浮动值
        on_hand_data = on_hand_data.astype(int)
        base_value_data = base_value_data.astype(int)

        # 进行列级别的相减
        result_row = on_hand_data - base_value_data

        # 将结果转换为一维数组
        result_array = result_row.values.flatten()  # 或者使用 result_row.to_numpy().flatten()

        return result_array

