import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


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

def read_and_process_file(good_file_path, map_file_path, distance_file_path):
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
    # Create DataFrame
    df = pd.DataFrame({
        'timestamp': timestamps,
        'x': xs,
        'y': ys,
        'value': values,
        'distances': distances_to_berths  # Store list of distances for each point
    })

    return df

class GA:
    """遗传算法"""

    def __init__(self, df, pc=0.6, pm=0.2, M=500, pop_size=50, length=10):
        self.df = df  # 数据集
        self.pc = pc  # 交叉概率
        self.pm = pm  # 突变概率
        self.length = len(df)     # 染色体长度，即二进制数组位数，默认为10
        self.pop_size = pop_size  # 种群（染色体）数，初始解的个数
        # self.pop = np.random.randint(0, 2, size=(pop_size, length))  # 随机初始化种群
        self.M = M  # 传递代数，这里选择50代

        # 50*2465
        self.pop = np.random.randint(2, size=(pop_size, len(df)), dtype=int) # 随机初始化种群
        # self.pop = np.zeros((pop_size, len(df)), dtype=int)  # 随机初始化种群
        self.fitnesses = np.zeros(self.pop_size)  # 适应度评估
        # self.fitness_eval(self.pop[0])

    def fitness_eval(self, chromo):
        robotStatus = np.zeros((2, 10), dtype=int)  # 1层是所处港口，2层是当前可控时间，默认全部停在0
        income = 0
        for itemId in range(len(chromo)):
            if chromo[itemId] == 1:
                itemReleaseTime = df['timestamp'][itemId]
                minTime = 200000000
                tarRobotId = -1
                tarWharfId = np.argmin(df['distances'][itemId])
                for robotId in range(10):
                    # 来不及取货
                    t1 = df['distances'][itemId][robotStatus[0][robotId]]
                    if t1 + robotStatus[1][robotId] > itemReleaseTime+1000:
                        continue
                    # 超时了送不到
                    t2 = df['distances'][itemId][tarWharfId]
                    if t1 + robotStatus[1][robotId] + t2 > 14500:
                        continue

                    if minTime > max(itemReleaseTime, t1 + robotStatus[1][robotId]):
                        minTime = max(itemReleaseTime, t1 + robotStatus[1][robotId])
                        tarRobotId = robotId
                if tarRobotId!=-1:
                    t2 = df['distances'][itemId][tarWharfId]
                    robotStatus[0][tarRobotId] = tarWharfId
                    robotStatus[1][tarRobotId] = minTime + t2
                    income += df['value'][itemId]
        return income

    def selection(self, pop):
        """对种群进行选择"""
        for i in range(self.pop_size):
            self.fitnesses[i] = self.fitness_eval(self.pop[i])
        idx = np.random.choice(np.arange(self.pop_size), replace=True, size=self.pop_size,
                               p=abs(self.fitnesses) / abs(self.fitnesses).sum())
        return pop[idx]

    @staticmethod
    def mutation(pop, pm):
        """对种群进行变异"""
        sx,  sy = pop.shape
        new_pop = np.zeros((sx, sy))
        for i in range(sx):  # x为种群个数
            if np.random.rand() < pm:
                m_point = np.random.randint(0, sy - 1)
                new_pop[i, :] = pop[i, :]
                if new_pop[i, m_point] == 0:
                    new_pop[i, m_point] = 1
                else:
                    new_pop[i, m_point] = 0
            else:
                new_pop[i, :] = pop[i, :]
        return new_pop

    @staticmethod
    def crossover(pop, pc):
        """对种群进行交叉"""
        sx, sy = pop.shape
        new_pop = np.zeros((sx, sy))
        for i in range(0, sx, 2):
            if np.random.rand() < pc:  # 以概率pc对染色体进行交叉
                c_point = np.random.randint(0, sy - 1)  # 随机选择交叉点cpoint
                new_pop[i, 0:c_point] = pop[i, 0:c_point]
                new_pop[i, c_point:sy] = pop[i + 1, c_point:sy]
                new_pop[i + 1, 0:c_point] = pop[i + 1, 0:c_point]
                new_pop[i + 1, c_point:sy] = pop[i, c_point:sy]
            else:
                new_pop[i, :] = pop[i, :]
                new_pop[i + 1, :] = pop[i, :]
        return new_pop

    def run(self):
        """主函数，把以上三个操作拼接起来"""
        for i in range(self.M):  # 进行M代的操作
            # print('the {} epoch'.format(i))  # 显示每一代
            # new_pop = self.selection(pop=self.pop)  # 选择
            new_pop = self.crossover(pop=self.pop, pc=self.pc)  # 交叉操作
            new_pop = self.mutation(pop=new_pop, pm=self.pm)  # 变异

            # 以下本质上就是selection操作
            pop = np.concatenate((self.pop, new_pop), axis=0)
            fitnesses = np.zeros(len(pop))
            for j in range(len(pop)):
                fitnesses[j] = self.fitness_eval(pop[j])
            idx = np.argsort(fitnesses)[::-1]
            for j in range(self.pop_size):
                self.fitnesses[j] = fitnesses[idx[j]]
                self.pop[j] = pop[idx[j]]

            print("Generation ", i, ": best fitness =",  max(self.fitnesses))
            print(sum(self.pop[0]))
        # new_pop = self.selection(pop=self.pop)


if __name__ == '__main__':
    good_file_path = 'map2_good.txt'
    map_file_path = 'map2.txt'
    distance_file_path = 'distances.txt'

    print("数据读取，整理……")
    df = read_and_process_file(good_file_path, map_file_path, distance_file_path)
    print("数据get完毕")

    g = GA(df)
    g.pc = 0.8   # 交叉概率
    g.pm = 0.3   # 突变概率
    g.M  = 100 # 迭代次数
    g.pop_size = 50 # 种群数量
    g.run()
