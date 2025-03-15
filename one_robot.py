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


def choose_goods(df, max_time=15000):
    robot_pos = (0, 0)  # 假设机器人起始位置为坐标(0,0)
    current_time = 0
    total_value = 0
    chosen_goods = []  # 记录选择的货物

    while current_time < max_time:
        # 计算当前位置到每个货物的距离
        df['distance_from_robot'] = np.sqrt((df['x'] - robot_pos[0]) ** 2 + (df['y'] - robot_pos[1]) ** 2)

        # 筛选出符合时间窗口条件的货物
        available_goods = df[(current_time + df['distance_from_robot'] <= df['timestamp'] + 1000) &
                             (current_time + df['distance_from_robot'] >= df['timestamp']) &
                             (df['choosed'] == 0)]

        if available_goods.empty:
            break  # 如果没有可选货物，结束循环

        # 选择价值最高的货物
        chosen_good = available_goods.loc[available_goods['value'].idxmax()]

        # 更新机器人状态
        robot_pos = (chosen_good['x'], chosen_good['y'])
        current_time += chosen_good['distance_from_robot']
        total_value += chosen_good['value']
        df.at[chosen_good.name, 'choosed'] = 1  # 更新货物的选择状态
        chosen_goods.append(chosen_good.name)

        if current_time >= max_time:
            break  # 超出时间限制，结束选择

    return df, chosen_goods, total_value

def getDistancesFromIndex(index):
    return df.iloc[index]['distances']

def dp_select_goods(df, current_berth, current_time, max_time, total_value,memo):
    # 基准情况：如果已经没有时间了
    if current_time >= max_time:
        return total_value, []

    # 存储每个候选货物的价值、路径和总距离
    candidates = []

    # 使用memo来避免重复计算
    if (current_berth, current_time) in memo:
        return memo[(current_berth, current_time)]

    max_value = total_value
    best_path = []

    for index, row in df.iterrows():
        if row['choosed'] == 1 or current_time < row['timestamp']:
            continue

        distances =getDistancesFromIndex(index)
        time_to_good=distances[current_berth]
        # 假设每个货物到最近港口的距离以及最近港口索引预先计算并存储
        nearest_berth_index = np.argmin(distances)
        time_to_berth = distances[nearest_berth_index]  # 到最近港口的时间
        current_berth=nearest_berth_index

        # 更新时间
        next_time = current_time + time_to_good

        if next_time < row['timestamp']:
            continue  # 如果不满足条件，则跳过此货物
        if next_time > max_time or next_time> row['timestamp'] + 1000:
            break
        next_time+=time_to_berth

        # 选择这个货物，递归搜索剩余的货物
        df.at[index, 'choosed'] = 1
        current_total_value = row['value'] + total_value
        value, path = dp_select_goods(df, nearest_berth_index, next_time, max_time, current_total_value, memo)
        df.at[index, 'choosed'] = 0  # 回溯，恢复状态

        if value > max_value:
            max_value = value
            # print("update max_value:",max_value)
            best_path = [(index, nearest_berth_index)] + path  # 记录货物索引和放置的港口位置
    # if current_time>14000:
    #     print("current_time:",current_time,"max_value:",max_value,"best_path:",best_path)
    memo[(current_berth, current_time)] = (max_value, best_path)
    return max_value, best_path


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

    df, chosen_goods, total_value = choose_goods(df)

    print("选取的货物ID：", chosen_goods)
    print("总价值：", total_value)

    memo = {}
    # 使用DP选择货物

    max_value, best_path = dp_select_goods(df, 0, 0, 15000,0, memo)

    print("选择的货物索引：", best_path)
    print("最大总价值：", max_value)