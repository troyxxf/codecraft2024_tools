import pandas as pd
import numpy as np
import copy
import matplotlib.pyplot as plt
import random
from collections import deque
from scipy.spatial.distance import cdist

class FAIndividual:
    # 种群个体
    def __init__(self, gene,length,endtime,param):
        # self.vardim = vardim
        self.length=length
        self.gene = gene
        self.endtime=endtime
        self.param=param
        self.fitness = 0
        self.trials = 0
        self.chrom = None

    def generage(self):
        self.gene=getRandomGene(self.length)[:]



    def calculateFitness(self):
        value=0
        robot_loc=[0 for i in range(10)]
        robot_time = [0 for i in range(10)]
        for i in range(self.length):
            if self.gene[i]==0: continue
            choose=-1
            busy=[]
            count=0
            while choose==-1:
                try_choose=chooseNearestRobot(getDistancesFromIndex(i),robot_loc,busy)
                if robot_time[try_choose]+getDistancesFromIndex(i)[robot_loc[try_choose]]<getTimeFromIndex(i)+1000:
                    if robot_time[try_choose] + getDistancesFromIndex(i)[robot_loc[try_choose]]<getTimeFromIndex(i):
                        robot_time[try_choose]=getTimeFromIndex(i)
                    else:
                        robot_time[try_choose]+=getDistancesFromIndex(i)[robot_loc[try_choose]]
                    nearest_beath=chooseNearestBerth(getDistancesFromIndex(i))
                    robot_loc[try_choose]=nearest_beath
                    robot_time[try_choose] += getDistancesFromIndex(i)[robot_loc[try_choose]]
                    choose=try_choose
                    value+=getValueFromIndex(i)
                else:
                    busy.append(try_choose)
                count+=1
                if count>=10:
                    # print("{}来不及运了，它的生成时间是{}，机器人{}的当前时间是{},距离是{}，要去{}港口的距离是{}".format(good_id,getTimeFromIndex(good_id),robot_id,robot_time[robot_id],getDistancesFromIndex(good_id)[robot_loc[robot_id]],berth_id,getDistancesFromIndex(good_id)[berth_id]))
                    break
            if min(robot_time)>=self.endtime:
                break
        # print(value)
        self.fitness=value

    def outputFitness(self):
        value = 0
        robot_loc = [0 for i in range(10)]
        robot_time = [0 for i in range(10)]
        line=[[] for i in range(10)]
        for i in range(self.length):
            if self.gene[i] == 0: continue
            choose = -1
            busy = []
            count = 0
            while choose == -1:
                try_choose = chooseNearestRobot(getDistancesFromIndex(i), robot_loc, busy)
                if robot_time[try_choose] + getDistancesFromIndex(i)[robot_loc[try_choose]] < getTimeFromIndex(
                        i) + 1000:
                    if robot_time[try_choose] + getDistancesFromIndex(i)[robot_loc[try_choose]] < getTimeFromIndex(i):
                        robot_time[try_choose] = getTimeFromIndex(i)
                    else:
                        robot_time[try_choose] += getDistancesFromIndex(i)[robot_loc[try_choose]]
                    nearest_beath = chooseNearestBerth(getDistancesFromIndex(i))
                    robot_loc[try_choose] = nearest_beath
                    robot_time[try_choose] += getDistancesFromIndex(i)[robot_loc[try_choose]]
                    choose = try_choose
                    value += getValueFromIndex(i)
                    line[try_choose].append(str(i))
                    line[try_choose].append(str(nearest_beath))
                else:
                    busy.append(try_choose)
                count += 1
                if count >= 10:
                    # print("{}来不及运了，它的生成时间是{}，机器人{}的当前时间是{},距离是{}，要去{}港口的距离是{}".format(good_id,getTimeFromIndex(good_id),robot_id,robot_time[robot_id],getDistancesFromIndex(good_id)[robot_loc[robot_id]],berth_id,getDistancesFromIndex(good_id)[berth_id]))
                    break
            if min(robot_time) >= self.endtime:
                break
        # print(value)
        self.fitness = value
        with open("result3.txt", 'a') as f:
            f.write(str(self.fitness))
            # line2=[",".join(tmp) for tmp in line]
            # line3=" ".join(line2)
            # f.write(line3)
            f.write(' '.join([str(item) for item in line]))
            f.write("\n")

class FireflyAlgorithm:
    def __init__(self,sizepop,length,MAXGEN,endtime,params):
        '''
        :param sizepop:种群数量
        :param length: 基因长度
        :param vardim: 维度
        :param gene: 基因--任务调度顺序
        :param endtime: 放弃搬运货物时间
        :param MAXGEN: 最大循环次数
        :param pareams: 参数 [beta,gamma,alpha]
        '''
        self.sizepop=sizepop
        self.length=length
        self.endtime=endtime
        # self.vardim=vardim
        # self.gene=gene
        self.MAXGEN = MAXGEN
        self.params = params
        self.population = [FAIndividual for i in range(self.sizepop)]
        self.fitness = np.zeros((self.sizepop, 1))
        self.trace = np.zeros((self.MAXGEN, 2))#用来画图

    def initialize(self):
        for i in range(0,self.sizepop):
            Gene=np.random.choice([0,1],size=self.length)
            ind=FAIndividual(Gene,self.length,self.endtime,self.params)
            ind.calculateFitness()
            self.population[i]=ind
            self.fitness[i]=ind.fitness
        # print("初始化的fitness",self.fitness)

    def evaluate(self):
        #evaluation of the population fitnesses
        fitnessZone=[]
        for i in range(0, self.sizepop):
            self.population[i].calculateFitness()
            fitnessZone.append(self.population[i].fitness)
        self.FitnessRenew(fitnessZone)

    def FitnessRenew(self,fitnessZone):
        # print("fitness before:",self.fitness)
        for i in range(len(fitnessZone)):
            self.fitness[i]=fitnessZone[i]

    def evolve(self):
        self.t = 0
        self.initialize()
        self.evaluate()
        best_fitness = np.max(self.fitness)
        bestIndex = np.argmax(self.fitness)
        self.best = copy.deepcopy(self.population[bestIndex])
        self.best.outputFitness()
        self.avefitness = np.mean(self.fitness)
        self.trace[self.t, 0] = self.best.fitness
        self.trace[self.t, 1] = self.avefitness
        print("Generation %d: optimal function value is: %f; average function value is %f" % (
            self.t, self.trace[self.t, 0], self.trace[self.t, 1]))
        while self.t < self.MAXGEN-1:
            self.t += 1
            self.move()
            self.evaluate()
            best_fitness = np.max(self.fitness)
            bestIndex = np.argmax(self.fitness)
            if best_fitness>self.best.fitness:#更新最优点
                self.best = copy.deepcopy(self.population[bestIndex])
                self.best.outputFitness()
            self.avefitness = np.mean(self.fitness)
            self.trace[self.t, 0] = self.best.fitness
            self.trace[self.t, 1] = self.avefitness
            print("Generation %d: optimal function value is: %f; average function value is %f" % (
                self.t, self.trace[self.t, 0], self.trace[self.t, 1]))
        print("Optimal function value is: %f; " %
              self.trace[self.t, 0])
        print("Optimal solution is:")
        print(self.best.gene)
        self.printResult()

#模仿萤火虫靠拢
    def move(self):
        NewFitness=[]
        for i in range(self.sizepop):
            ran=random.random()
            #参数1的概率不动
            if ran<self.population[i].param[1]:
                continue
            else:
                for j in range(self.sizepop):
                    #靠近
                    if self.population[i].fitness<self.population[j].fitness:
                        mask=np.random.rand(self.length)<self.population[i].param[0]
                        self.population[i].gene[mask]=self.population[j].gene[mask]
                        self.population[i].calculateFitness()

#随机扰动，参数2的概率重新生成基因
        for i in range(self.sizepop):
            ran=random.random()
            if(ran<self.population[i].param[2]):
                self.population[i].gene =np.random.choice([0,1],size=self.length)
        #更新fitness
        self.evaluate()






    def printResult(self):
        '''
        plot the result of the firefly algorithm
        '''
        x = np.arange(0, self.MAXGEN)
        y1 = self.trace[:, 0]
        y2 = self.trace[:, 1]
        plt.plot(x, y1, 'r', label='optimal value')
        plt.plot(x, y2, 'g', label='average value')
        plt.xlabel("Iteration")
        plt.ylabel("function value")
        plt.title("Firefly Algorithm for function optimization")
        plt.legend()
        plt.show()

def getValueFromIndex(index):
    return df.iloc[index]['value']

def getTimeFromIndex(index):
    return df.iloc[index]['timestamp']

def getDistancesFromIndex(index):
    return df.iloc[index]['distances']

def chooseNearestRobot(distances,robot_loc,busy):
    to_robot_distances=[distances[robot_loc[i]] for i in range(10)]
    if len(busy)>0:
        for id in busy:
            to_robot_distances[id]=10000
    return to_robot_distances.index(min(to_robot_distances))#返回机器人id

def chooseNearestBerth(distances):
    return distances.index(min(distances))#返回机器人id

#找两个列表中相同个数
def count_common_elements(list1, list2):
    """
    Count the number of common elements between two lists without converting them to sets.
    Returns:
    - An integer representing the count of common elements between the two lists.
    """
    common_count = 0
    for element in list1:
        if element in list2:
            common_count += 1
    return common_count


def regenerate_list_b(list_a, list_large, list_b):
    """
    Regenerate list B to have the same common elements with list A, and replace other elements randomly from the large list.
    - A new list B with the same common elements with list A, plus additional random elements from the large list.
    """
    # Find common elements between list A and list B
    common_elements = [element for element in list_b if element in list_a]

    # Calculate how many new elements are needed to fill list B
    num_new_elements = len(list_b) - len(common_elements)

    # Ensure the large list has unique elements not already in list B
    unique_large_elements = [element for element in list_large if element not in list_b]

    # Randomly select new elements to add to list B
    new_elements = random.sample(unique_large_elements, num_new_elements)

    # Combine common elements with new elements to form the new list B
    new_list_b = common_elements + new_elements
    selected_indices=df.iloc[new_list_b].sort_values(by='timestamp')
    ans=[]
    for i in range(len(selected_indices)):
        ans.append(selected_indices.iloc[i].name)
    return ans
#选择货物id
def getRandomGene(length):
    return np.random.choice([0,1],size=length)


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
    # Create DataFrame
    df = pd.DataFrame({
        'timestamp': timestamps,
        'x': xs,
        'y': ys,
        'value': values,
        'distances': distances_to_berths  # Store list of distances for each point
    })

    return df

def add_random_distances(df, seed=42):
    """
    Adds a column of random distances to the DataFrame.
    """
    # np.random.seed(seed)
    df['distance'] = np.random.randint(15, 131, size=len(df))


def get_sorted_random_subset(df, num_rows, seed=42):
    """
    Returns a sorted subset of the DataFrame based on random indexes.
    """
    # np.random.seed(seed)
    random_indexes = np.random.choice(len(df), min(num_rows, len(df)), replace=False)
    return df.iloc[random_indexes].sort_values(by='timestamp')


def select_random_indices_in_time_range(df, t1, t2, k):
    """
    Selects k random indices from df where the timestamp is between t1 and t2.

    Parameters:
    - df: Pandas DataFrame with a 'timestamp' column.
    - t1: Start time of the range.
    - t2: End time of the range.
    - k: Number of indices to select.

    Returns:
    A list of k random indices from df where t1 <= timestamp <= t2. If there are
    fewer than k indices in the range, returns all available indices.
    """
    # Filter the DataFrame for rows where the timestamp is between t1 and t2
    filtered_df = df[(df['timestamp'] >= t1) & (df['timestamp'] <= t2)]

    # Get the indices of the filtered DataFrame
    indices = filtered_df.index.tolist()

    # Randomly select k indices from the filtered list, without replacement
    # If there are fewer than k indices available, select all of them
    selected_indices = np.random.choice(indices, min(k, len(indices)), replace=False)
    selected_indices=df.iloc[selected_indices].sort_values(by='timestamp')
    list = []
    for i in range(len(selected_indices)):
        list.append(selected_indices.iloc[i].name)
    return list

def getPartGene(list):

    choose_robot = [np.random.randint(0, 10) for i in range(len(list))]
    choose_berth = [np.random.randint(0, 10) for i in range(len(list))]
    PartGene = []
    for i in range(len(list)):
        tmp = []
        tmp.append(choose_robot[i])
        tmp.append(choose_berth[i])
        tmp.append(list[i])
        PartGene.append(tmp)
    return PartGene
#计算到各个港口的距离
def bfs(matrix, start, end):
    """
    Perform BFS to find the shortest path from start to end.
    start and end are given as (x, y).
    """
    if start == end:
        return 0  # Start and end are the same

    rows, cols = len(matrix), len(matrix[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, left, down, up
    visited = set([start])
    queue = deque([(start, 0)])  # ((x, y), distance)

    while queue:
        (x, y), dist = queue.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and (
                    matrix[ny][nx] == '.' or matrix[ny][nx] == 'A' or matrix[ny][nx] == 'B') and (
            nx, ny) not in visited:
                if (nx, ny) == end:
                    return dist + 1  # Found the end, return distance
                visited.add((nx, ny))
                queue.append(((nx, ny), dist + 1))

    return -1  # If end is not reachable from start
def load_matrix_and_calculate_distances(file_path, harbors_centers, start):
    # Load the map into a matrix
    with open(file_path, 'r') as file:
        matrix = [list(line.strip()) for line in file]
    # Calculate distances to each harbor center from start
    distances = [bfs(matrix, start, harbor) for harbor in harbors_centers]
    return distances

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

    # Main
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

    # fa=FAIndividual
    # fa.generage()
    # print(fa.gene())

    # fa=

    # Get a sorted subset of the DataFrame based on 30 random indexes
    # sorted_subset_df = get_sorted_random_subset(df, 30)

    # choose_robot=[np.random.randint(0, 10) for i in range(len(sorted_subset_df))]
    # choose_berth=[np.random.randint(0, 10) for i in range(len(sorted_subset_df))]
    list_large = df.index.tolist()

    sizepop=100 #种群数量
    length=len(df) #基因长度
    MAXGEN=100 #最大循环次数
    endtime=14000#因为目前跑的1000帧的，所以是1000 跑全部应该改到14200
    pareams=[0.7,0.01,0.001] #参数[beta, gamma, alpha]
    FA=FireflyAlgorithm(sizepop,length,MAXGEN,endtime,pareams)
    FA.initialize()
    # # for fa in FA.population:
    # #     print(len(fa.gene))
    FA.evolve()
    # fa=FAIndividual(np.random.choice([0,1],size=length),length,endtime,pareams)
    # fa.calculateFitness()
    # print(fa.fitness)




    # print(df.iloc[10]['value'])
