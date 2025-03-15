# 假设数据已经加载到distance.txt中，我们将读取文件，并按货物ID组织距离信息到列表中

# 读取数据文件并解析
distance_file_path = 'out(3).txt'

distances_by_goods = {}

with open(distance_file_path, 'r') as file:
    for line in file:
        berth_id, goods_id, distance = map(int, line.split())
        if goods_id not in distances_by_goods:
            distances_by_goods[goods_id] = []
        distances_by_goods[goods_id].append(distance)

# 转换成列表，索引即货物ID，每个元素是对应货物到所有泊位的距离列表
distances_list = [distances_by_goods[goods_id] for goods_id in sorted(distances_by_goods.keys())]

print(distances_list)
