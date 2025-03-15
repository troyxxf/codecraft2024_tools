import matplotlib.pyplot as plt
import pandas as pd

# 读取数据
# with open('goods_data.txt', 'r') as file:
#     lines = file.readlines()
with open('goods正1.txt', 'r') as file:
    lines = file.readlines()

# 解析数据
data = {'Time': [], 'X': [], 'Y': [], 'Value': []}
for line in lines:
    time, xy, value = line.split()
    x, y = map(int, xy.split(','))
    data['Time'].append(int(time))
    data['X'].append(x)
    data['Y'].append(y)
    data['Value'].append(int(value))

# 转换为DataFrame
df = pd.DataFrame(data)

value_0_100 = df[(df['Value'] >= 0) & (df['Value'] <= 100)]
value_175_200 = df[(df['Value'] >= 175) & (df['Value'] <= 200)]
value_180_190 = df[(df['Value'] >= 180) & (df['Value'] <= 190)]
value_190_200 = df[(df['Value'] >= 190) & (df['Value'] < 200)]
value_total=df

count_0_100 = len(value_0_100)
count_175_200 = len(value_175_200)
count_total=len(value_total)
count_180_190=len(value_180_190)
count_190_200=len(value_190_200)

print("0-100:",count_0_100,"175-200:", count_175_200," total:",count_total)
print("180_190",count_180_190,"190_200:",count_190_200)
print("总价值",sum(value_total['Value']))

# 创建图像
fig, ax = plt.subplots(3, 1, figsize=(10, 15))

# 时间与价值的关系
ax[0].scatter(df['Time'], df['Value'], c='blue')
ax[0].set_title('Time vs Value')
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Value')

# 坐标与价值的关系
scatter = ax[1].scatter(df['X'], df['Y'], c=df['Value'], cmap='viridis')
ax[1].set_title('Coordinates vs Value')
ax[1].set_xlabel('X')
ax[1].set_ylabel('Y')
fig.colorbar(scatter, ax=ax[1], label='Value')

# 时间与坐标的关系
scatter2 = ax[2].scatter(df['X'], df['Y'], c=df['Time'], cmap='plasma')
ax[2].set_title('Coordinates vs Time')
ax[2].set_xlabel('X')
ax[2].set_ylabel('Y')
fig.colorbar(scatter2, ax=ax[2], label='Time')

plt.tight_layout()
plt.show()

# 计算每个时间点的价值数量
value_counts = df.groupby('Time')['Value'].count()

# 统计每个时间点的数量
time_counts = df['Time'].value_counts().sort_index()

# 画图
plt.figure(figsize=(25, 6))
time_counts.plot(kind='bar')
plt.title('Number of Points at Each Time')
plt.xlabel('Time')
plt.ylabel('Number of Points')
plt.tight_layout()
plt.show()

#预测
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_squared_error
#
# # 准备数据
# X = df[['Time']] # 使用时间作为特征
# y = df[['X', 'Y', 'Value']] # 预测X, Y坐标和价值
#
# # 划分训练集和测试集
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#
# # 初始化并训练模型
# model = RandomForestRegressor(n_estimators=100, random_state=42)
# model.fit(X_train, y_train)
#
# # 进行预测
# y_pred = model.predict(X_test)
#
# # 评估模型
# mse = mean_squared_error(y_test, y_pred)
# print(f'Mean Squared Error: {mse}')
#
# # 预测未来的点
# # 例如，预测时间为160的点的位置和价值
# future_time = [[14994]]
# future_pred = model.predict(future_time)
# print(f'Predicted X, Y coordinates and Value for time 160: {future_pred}')

# # 根据区间过滤数据
# quadrant_1 = df[(df['X'] <= 100) & (df['Y'] <= 100)]
# quadrant_2 = df[(df['X'] <= 100) & (df['Y'] > 100)]
# quadrant_3 = df[(df['X'] > 100) & (df['Y'] <= 100)]
# quadrant_4 = df[(df['X'] > 100) & (df['Y'] > 100)]
#
# # 绘制每个区间内时间与价值的关系图
# fig, axes = plt.subplots(2, 2, figsize=(12, 12))
#
# axes[0, 0].scatter(quadrant_1['Time'], quadrant_1['Value'], c='red')
# axes[0, 0].set_title('Quadrant 1: Time vs Value')
# axes[0, 0].set_xlabel('Time')
# axes[0, 0].set_ylabel('Value')
#
# axes[0, 1].scatter(quadrant_2['Time'], quadrant_2['Value'], c='green')
# axes[0, 1].set_title('Quadrant 2: Time vs Value')
# axes[0, 1].set_xlabel('Time')
# axes[0, 1].set_ylabel('Value')
#
# axes[1, 0].scatter(quadrant_3['Time'], quadrant_3['Value'], c='blue')
# axes[1, 0].set_title('Quadrant 3: Time vs Value')
# axes[1, 0].set_xlabel('Time')
# axes[1, 0].set_ylabel('Value')
#
# axes[1, 1].scatter(quadrant_4['Time'], quadrant_4['Value'], c='purple')
# axes[1, 1].set_title('Quadrant 4: Time vs Value')
# axes[1, 1].set_xlabel('Time')
# axes[1, 1].set_ylabel('Value')
#
# plt.tight_layout()
# plt.show()

# import pandas as pd
#
# # Assuming the data is structured correctly in goods_data.txt:
# # Time X,Y Value
#
# # Read and parse the file content
# with open("./goods_data.txt", "r", encoding="ascii") as file:
#     lines = file.readlines()
#
# data_parsed = []
# for line in lines:
#     parts = line.strip().split()
#     if len(parts) == 3:  # Ensuring the correct format of Time, Coordinates, Value
#         time, coords, value = parts
#         x, y = map(int, coords.split(','))  # Splitting the coordinates and converting to integers
#         data_parsed.append({'Time': int(time), 'X': x, 'Y': y, 'Value': int(value)})
#
# # Create a DataFrame from the parsed data
# df = pd.DataFrame(data_parsed)
#
# # Group by coordinates and find different times for each location
# grouped = df.groupby(['X', 'Y'])
#
# # Find out the different times corresponding to each position
# time_by_coordinates = grouped['Time'].apply(lambda x: x.unique().tolist())
#
# # Find those positions that have multiple time points
# multiple_times = time_by_coordinates[time_by_coordinates.apply(len) > 1]
#
# # Output these positions and their corresponding times
# multiple_times.to_frame().reset_index().to_csv("./multiple_times.csv", index=False)


