from collections import deque
import numpy as np

# 初始化参数
num_ports = 10  # 假设港口总数

def read_port_events(file_path):
    port_events = {port_id: [] for port_id in range(num_ports)}  # 假设码头ID从0开始编号
    with open(file_path, 'r') as file:
        for line in file:
            generation_time, port_id, cargo_value = map(int, line.split())
            port_events[port_id].append((generation_time, cargo_value))
    return port_events

def output_when_reached_N(port_events, N):
    port_cargo_count = {port_id: 0 for port_id in range(num_ports)}  # 记录每个港口的货物数量
    port_values = {port_id: 0 for port_id in range(num_ports)}  # 记录每个港口的总价值

    for port_id, events in port_events.items():
        for time, value in events:
            port_cargo_count[port_id] += 1
            port_values[port_id] += value

            # 当货物数量达到N时，输出时间、港口ID和总价值，并重置计数器和总价值
            if port_cargo_count[port_id] == N:
                print(f"Time: {time}, Port ID: {port_id}, Total Value: {port_values[port_id]}")
                port_cargo_count[port_id] = 0  # 重置货物数量，如果需要持续跟踪
                port_values[port_id] = 0  # 重置总价值，如果需要持续跟踪

# 路径替换为你的文件路径
file_path = 'time_id_value.txt'
port_events = read_port_events(file_path)

# 假设N为阈值，例如3
N = 71
output_when_reached_N(port_events, N)

# ships_schedules = [
#     {'travel_time': 1320, 'schedule': [2, , 2, 3, 4]},
#     {'travel_time': 1000, 'schedule': [1, 2, 3, 4, 0]},
#     {'travel_time': 1070, 'schedule': [2, 3, 4, 0, 1]},
#     {'travel_time': 850, 'schedule': [3, 4, 0, 1, 2]},
#     {'travel_time': 850, 'schedule': [4, 0, 1, 2, 3]},
# ]

def simulate_ships_schedule(ships_schedules, port_events, N):
    for ship_idx, ship in enumerate(ships_schedules):
        current_time = 0  # 初始时间
        for port_id in ship['schedule']:
            # 等待直到港口的货物数量达到N
            while len(port_events[port_id]) < N:
                # 假设货物是按时间顺序生成的，这里简化为直接跳到下一个货物生成时间
                if port_events[port_id]:
                    next_time, _ = port_events[port_id][min(N-1, len(port_events[port_id])-1)]
                    current_time = max(current_time, next_time)
                else:
                    break  # 如果这个港口没有更多事件，跳出循环

            # 计算到达和离开的时间
            arrive_time = current_time + ship['travel_time']
            leave_time = arrive_time  # 在这个示例中，假设船只离开的时间即为到达时间

            print(f"Ship {ship_idx + 1} arrives at port {port_id} at time {arrive_time}, leaves at time {leave_time}")

            # 更新当前时间为离开时间加上前往下一个港口的运输时间
            current_time = leave_time + ship['travel_time']



num_ports = 10  # 总港口数量
N = 3  # 指定的货物数量阈值

# 船只的调度顺序和运输时间
ships_schedules = [
    {'travel_time': 1320, 'schedule': [0, 0, 2]},
    {'travel_time': 1000, 'schedule': [5, 2, 8]},
    {'travel_time': 1070, 'schedule': [1, 8, 3]},
    {'travel_time': 850, 'schedule': [9, 4, 7]},
    {'travel_time': 850, 'schedule': [3, 2, 3]},
]

# 读取港口事件数据
port_events = read_port_events(file_path)

# 模拟船只的调度过程
def simulate_ships_schedule(ships_schedules, port_events, N):
    for ship_idx, ship in enumerate(ships_schedules):
        current_time = 0  # 初始时间
        for port_id in ship['schedule']:
            # 等待直到港口的货物数量达到N
            while len(port_events[port_id]) < N:
                # 假设货物是按时间顺序生成的，这里简化为直接跳到下一个货物生成时间
                if port_events[port_id]:
                    next_time, _ = port_events[port_id][min(N-1, len(port_events[port_id])-1)]
                    current_time = max(current_time, next_time)
                else:
                    break  # 如果这个港口没有更多事件，跳出循环

            # 计算到达和离开的时间
            arrive_time = current_time + ship['travel_time']
            leave_time = arrive_time  # 在这个示例中，假设船只离开的时间即为到达时间

            print(f"Ship {ship_idx + 1} arrives at port {port_id} at time {arrive_time}, leaves at time {leave_time}")

            # 更新当前时间为离开时间加上前往下一个港口的运输时间
            current_time = leave_time + ship['travel_time']

# 运行模拟
simulate_ships_schedule(ships_schedules, port_events, N)

