import pandas as pd
import numpy as np
import copy
import matplotlib.pyplot as plt
import random
from collections import deque
from scipy.spatial.distance import cdist

def read_and_process_file(good_file_path,map_file_path,distance_file_path):
    timestamps, xs, ys, values = [], [], [], []
    distances_to_berths = read_distance_file(distance_file_path)
    with open(good_file_path, 'r') as file:
        for line in file:
            parts = line.split()  # Split by space
            timestamp, xy, value = parts[0], parts[1], parts[2]

            x, y = map(int, xy.split(','))  # Convert x and y to integers

            timestamps.append(int(timestamp))
            xs.append(x)
            ys.append(y)
            values.append(int(value))
            choosed=0
    # Create DataFrame
    df = pd.DataFrame({
        'timestamp': timestamps,
        'x': xs,
        'y': ys,
        'value': values,
        'distances': distances_to_berths,  # Store list of distances for each point
        'choosed':choosed
    })

    return df
def read_distance_file(distance_file_path):
    distances_by_goods = {}
    with open(distance_file_path, 'r') as file:
        for line in file:
            berth_id, goods_id, distance = map(int, line.split())
            if goods_id not in distances_by_goods:
                distances_by_goods[goods_id] = []
            distances_by_goods[goods_id].append(distance)

    # 转换成列表，索引即货物ID，每个元素是对应货物到所有泊位的距离列表
    distances_list = [distances_by_goods[goods_id] for goods_id in sorted(distances_by_goods.keys())]
    return distances_list

def getDistancesFromIndex(index):
    return df.iloc[index]['distances']

def dp_select_goods(df, current_berth, current_time, max_time, total_value, memo):
    # 基准情况
    if current_time >= max_time:
        return total_value, []

    # 查看是否已计算过此状态
    memo_key = (current_berth, current_time)
    if memo_key in memo:
        return memo[memo_key]

    candidate_goods = []

    # 筛选和评估货物
    for index, row in df.iterrows():
        if row['choosed'] == 1:
            continue

        distances = getDistancesFromIndex(index)
        time_to_good = distances[current_berth]
        next_time = current_time + time_to_good

        if row['timestamp'] <= next_time <= row['timestamp'] + 1000:
            nearest_berth_index = np.argmin(distances)
            time_to_berth = distances[nearest_berth_index]
            total_distance = time_to_good + time_to_berth
            if next_time + time_to_berth <= max_time:
                candidate_goods.append((index, row['value'], total_distance, nearest_berth_index, next_time + time_to_berth))

    # 根据价值降序和距离升序排序
    candidate_goods.sort(key=lambda x: (-x[1], x[2]))

    # 只选择前三个最优货物进行递归
    max_value = total_value
    best_path = []

    for candidate in candidate_goods[:1]:
        index, value, _, nearest_berth_index, new_time = candidate
        df.at[index, 'choosed'] = 1
        new_total_value, path = dp_select_goods(df, nearest_berth_index, new_time, max_time, total_value + value, memo)
        df.at[index, 'choosed'] = 0  # 回溯

        if new_total_value > max_value:
            max_value = new_total_value
            best_path = [(index, nearest_berth_index)] + path

    memo[memo_key] = (max_value, best_path)
    return max_value, best_path

def update_choosed_goods(df, best_path):
    for index, _ in best_path:
        df.at[index, 'choosed'] = 1

if __name__ == "__main__":
    # File path
    good_file_path = 'map2_good.txt'
    map_file_path = 'map2.txt'
    distance_file_path = 'distances.txt'

    #berth_loc=[(68, 62), (88, 62), (112, 62), (138, 70), (62, 84), (138, 88), (62, 88), (62, 104), (62, 110), (88, 138)]

    print("数据读取，整理……")
    # Process the file to create a DataFrame
    df = read_and_process_file(good_file_path,map_file_path,distance_file_path)

    print("数据get完毕")
    print(len(df))
    #


    robot_number=20
    for i in range(robot_number):
        memo = {}
        # 使用DP选择货物
        max_value, best_path = dp_select_goods(df, 0, 0, 15000,0, memo)
        print(i,"选择的货物索引：", best_path)
        print(i,"最大总价值：", max_value)
        update_choosed_goods(df, best_path)
