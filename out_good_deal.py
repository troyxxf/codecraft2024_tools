import matplotlib.pyplot as plt
import statistics

def read_data(file_path):
    goods_data = []
    robot_data = []

    with open(file_path, 'r') as file:
        for line in file:
            # Splitting line by whitespace
            data = line.strip().split()
            if len(data) == 3:
                # Assuming time, x, y, value for goods data
                zuobiao=data[1].strip().split(",")
                x=zuobiao[0]
                y=zuobiao[1]
                goods_data.append((int(data[0]), x, x, int(data[2])))
            elif len(data) == 4:
                # Assuming time, id, port number, price for robot data
                robot_data.append((int(data[0]), int(data[1]), int(data[2]), int(data[3])))

    return goods_data, robot_data

file_path = 'out_good0316.txt'
goods_data, robot_data = read_data(file_path)

time_goods = [item[0] for item in goods_data]
value_goods = [item[3] for item in goods_data]

value_0_100 = [i for i in value_goods if i<=100 and i>=0]
value_175_200 = [i for i in value_goods if i<=200 and i>=175]
print("0-100",len(value_0_100))
print("175-200",len(value_175_200))

plt.figure(figsize=(10, 5))
plt.scatter(time_goods, value_goods)
plt.title('Goods Value over Time')
plt.xlabel('Time')
plt.ylabel('Value')
plt.grid(True)
plt.show()

# Plotting robot data
time_robot = [item[0] for item in robot_data]
price_robot = [item[3] for item in robot_data]

plt.figure(figsize=(10, 5))
plt.scatter(time_robot, price_robot)
plt.title('Robot Price over Time')
plt.xlabel('Time')
plt.ylabel('Price')
plt.grid(True)
plt.show()

value_goods.sort()
print("中位数为：",statistics.median(value_goods))

print("总生成货物价值为:",sum(value_goods)," 个数为：",len(value_goods),"平均值为：",sum(value_goods)/len(value_goods))
print("总搬运货物价值为:",sum(price_robot)," 个数为：",len(price_robot),"平均值为：",sum(price_robot)/len(price_robot))
print("搬运货物比总货物价值：",sum(price_robot)/sum(value_goods)," 个数比",len(price_robot)/len(value_goods))