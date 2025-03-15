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
        self.length = len(df)  # 染色体长度，即二进制数组位数，默认为10
        self.pop_size = pop_size  # 种群（染色体）数，初始解的个数
        # self.pop = np.random.randint(0, 2, size=(pop_size, length))  # 随机初始化种群
        self.M = M  # 传递代数，这里选择50代

        self.pop = np.random.uniform(low=0, high=1, size=(pop_size, 2, self.length))  # 随机初始化种群
        self.fitnesses = np.zeros(self.pop_size)  # 适应度评估
        # for i in range(self.pop_size):
        #     self.fitnesses[i] = self.fitness_eval(self.pop[i])

    def fitness_eval(self, chromo):
        # idx = np.argsort(chromo[1][:])[::-1]
        idx = np.arange(self.length)
        tasks = -np.ones((10, self.length, 2), dtype=int)
        hisid = np.zeros(10, dtype=int)
        for i in idx:  # i其实就是货物的id
            taskId = int(np.floor(chromo[0][i] * 100))
            robotId = int(np.floor(taskId / 10))
            wharfId = int(taskId % 10)
            tasks[robotId][hisid[robotId]][0] = i
            tasks[robotId][hisid[robotId]][1] = wharfId
            hisid[robotId] += 1

        totalIncome = 0
        robotPos = np.zeros(10, dtype=int)  # 假设所有的机器人初始化全在0号码头
        for robotId in range(10):
            # print("robot: ", robotId)
            i = 0
            currentTime = 0
            income = 0
            while tasks[robotId][i][0] != -1 and currentTime < 15000:
                itemId = tasks[robotId][i][0]
                wharfId = tasks[robotId][i][1]
                t1 = df['distances'][itemId][robotPos[robotId]]  # 机器人从码头到物品取货时间
                t2 = df['distances'][itemId][wharfId]  # 机器人取货后送货到码头时间
                itemReleaseTime = df['timestamp'][itemId]
                if itemReleaseTime + 1000 < t1 + currentTime:  # 来不及取货
                    i += 1
                    continue
                # 取货成功
                currentTime = max(itemReleaseTime + 1000, currentTime + t1) + t2
                robotPos[robotId] = wharfId
                if currentTime < 15000:  # 送货成功
                    income += df['value'][itemId]
                    # print(income)
                else:
                    break
                i += 1
            totalIncome += income
        # print(totalIncome)
        return totalIncome

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
        sx, sz, sy = pop.shape
        new_pop = np.zeros((sx, sz, sy))
        for i in range(sx):  # x为种群个数
            if np.random.rand() < pm:
                m_point = np.random.randint(0, sy - 1)
                new_pop[i, :, :] = pop[i, :, :]
                new_pop[i, 0, m_point] = np.random.uniform(0, 1)  # 1层变异
                new_pop[i, 1, m_point] = np.random.uniform(0, 1)  # 2层变异
                #
                # if new_pop[i, m_point] == 0:
                #     new_pop[i, m_point] = 1
                # else:
                #     new_pop[i, m_point] = 0
            else:
                new_pop[i, :, :] = pop[i, :, :]
        return new_pop

    @staticmethod
    def crossover(pop, pc):
        """对种群进行交叉"""
        """我们是三维的"""
        sx, sz, sy = pop.shape
        new_pop = np.zeros((sx, sz, sy))
        for i in range(0, sx, 2):
            if np.random.rand() < pc:  # 以概率pc对染色体进行交叉
                c_point = np.random.randint(0, sy - 1)  # 随机选择交叉点cpoint
                # 1层交叉
                new_pop[i, 0, 0:c_point] = pop[i, 0, 0:c_point]
                new_pop[i, 0, c_point:sy] = pop[i + 1, 0, c_point:sy]
                new_pop[i + 1, 0, 0:c_point] = pop[i + 1, 0, 0:c_point]
                new_pop[i + 1, 0, c_point:sy] = pop[i, 0, c_point:sy]

                # 2层交叉
                new_pop[i, 1, 0:c_point] = pop[i, 1, 0:c_point]
                new_pop[i, 1, c_point:sy] = pop[i + 1, 1, c_point:sy]
                new_pop[i + 1, 1, 0:c_point] = pop[i + 1, 1, 0:c_point]
                new_pop[i + 1, 1, c_point:sy] = pop[i, 1, c_point:sy]
            else:
                new_pop[i, :, :] = pop[i, :, :]
                new_pop[i + 1, :, :] = pop[i, :, :]
        return new_pop

    def run(self):
        """主函数，把以上三个操作拼接起来"""
        for i in range(self.M):  # 进行M代的操作
            # print('the {} epoch'.format(i))  # 显示每一代
            # new_pop = self.selection(pop=self.pop)  # 选择
            new_pop = self.crossover(pop=self.pop, pc=self.pc)  # 交叉操作
            new_pop = self.mutation(pop=new_pop, pm=self.pm)  # 变异

            pop = np.concatenate((self.pop, new_pop), axis=0)
            fitnesses = np.zeros(len(pop))
            for i in range(len(pop)):
                fitnesses[i] = self.fitness_eval(pop[i])
            idx = np.argsort(fitnesses)[::-1]
            for i in range(self.pop_size):
                self.fitnesses[i] = fitnesses[idx[i]]
                self.pop[i] = pop[idx[i]]

            print(max(self.fitnesses))
        # new_pop = self.selection(pop=self.pop)


if __name__ == '__main__':
    good_file_path = 'map1_good.txt'
    map_file_path = 'mapmap1.txt'
    distance_file_path = 'out(map1).txt'

    print("数据读取，整理……")
    df = read_and_process_file(good_file_path, map_file_path, distance_file_path)
    print("数据get完毕")

    g = GA(df)
    g.run()
