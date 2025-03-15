import logging
import sys
import random
n = 200
robot_num = 10
berth_num = 10
N = 210
class Robot:
    def __init__(self, startX=0, startY=0, goods=0, status=0, mbx=0, mby=0):
        self.x = startX
        self.y = startY
        self.goods = goods
        self.status = status
        self.mbx = mbx
        self.mby = mby

robot = [Robot() for _ in range(robot_num + 10)]

class Berth:
    def __init__(self, x=0, y=0, transport_time=0, loading_speed=0):
        self.x = x
        self.y = y
        self.transport_time = transport_time
        self.loading_speed = loading_speed

berth = [Berth() for _ in range(berth_num + 10)]

class Boat:
    def __init__(self, num=0, pos=0, status=0):
        self.num = num
        self.pos = pos
        self.status = status

boat = [Boat() for _ in range(10)]


money = 0
boat_capacity = 0
id = 0
ch = []
gds = [[0 for _ in range(N)] for _ in range(N)]
goods_info=[]

#转四进制
def decimal_to_quaternary_with_padding(num, min_length):
    quaternary_str = ""
    while num > 0:
        remainder = num % 4
        quaternary_str = str(remainder) + quaternary_str
        num //= 4

    # Add leading zeros if the length is less than min_length
    if len(quaternary_str) < min_length:
        quaternary_str = quaternary_str.rjust(min_length, '0')

    return quaternary_str

def Init():
    for i in range(0, n):
        line = input()
        ch.append([c for c in line.split(sep=" ")])
    for i in range(berth_num):
        line = input()
        berth_list = [int(c) for c in line.split(sep=" ")]
        id = berth_list[0]
        berth[id].x = berth_list[1]
        berth[id].y = berth_list[2]
        berth[id].transport_time = berth_list[3]
        berth[id].loading_speed = berth_list[4]
    boat_capacity = int(input())
    okk = input()
    print("OK")
    sys.stdout.flush()
def Input():
    id, money = map(int, input().split(" "))
    num = int(input())
    for i in range(num):
        x, y, val = map(int, input().split())
        gds[x][y] = val
        gd_info=[]#时间、x,y,价值
        gd_info.append(id)
        gd_info.append(x)
        gd_info.append(y)
        gd_info.append(val)
    for i in range(robot_num):
        robot[i].goods, robot[i].x, robot[i].y, robot[i].status = map(int, input().split())
    for i in range(5):
        boat[i].status, boat[i].pos = map(int, input().split())
    okk = input()
    return id

def Robot2Move(i,dem,list):
    if dem==0:
        print("move", i, dem)
        sys.stdout.flush()
        list[i]=1
    elif dem==1:
        print("move", i, dem)
        sys.stdout.flush()
        list[i]=0
    elif dem==2:
        print("move", i, dem)
        sys.stdout.flush()
        list[i]=3
    elif dem==3:
        print("move", i, dem)
        sys.stdout.flush()
        list[i]=2

def Robot2Move2(i,dem,list):
    if dem==0:
        print("move", i+5, dem)
        sys.stdout.flush()
        list[i+5]=1
    elif dem==1:
        print("move", i+5, dem )
        sys.stdout.flush()
        list[i+5]=0
    elif dem==2:
        print("move", i+5, dem)
        sys.stdout.flush()
        list[i+5]=3
    elif dem==3:
        print("move", i+5, dem)
        sys.stdout.flush()
        list[i+5]=2

if __name__ == "__main__":
    Init()
    gd_count=0
    flag=0
    re_robot=[-1 for i in range(10)]
    for zhen in range(1, 15001):
        id = Input()
        robot
        #输出时间
        if flag==0:
            if gd_count>len(goods_info)-1:
                continue
            time=goods_info[gd_count][0]
            str_time=decimal_to_quaternary_with_padding(time,7)
            for i in range(7):
                Robot2Move(i,int(str_time[i]),re_robot)
            flag=1
            continue
        #复位
        elif flag==1:

            for i in range(len(re_robot)):
                if re_robot[i] !=-1:
                    print("move", i, re_robot[i])
                    sys.stdout.flush()
                    re_robot[i] = -1
            flag=2
            continue
        # 货物的位置信息
        elif flag==2:
            x_info=goods_info[gd_count][1]
            str_x=decimal_to_quaternary_with_padding(x_info,5)
            for i in range(5):
                Robot2Move(i, int(str_x[i]), re_robot)
            y_info=goods_info[gd_count][2]
            str_y=decimal_to_quaternary_with_padding(y_info,5)
            for i in range(5):
                Robot2Move2(i, int(str_y[i]), re_robot)
            flag=3
            continue
        #复位
        elif flag==3:
            for i in range(len(re_robot)):
                if re_robot[i] !=-1:
                    print("move", i, re_robot[i])
                    sys.stdout.flush()
                    re_robot[i] = -1
            flag=4
            continue
        #价值信息
        elif flag==4:
            value_info=goods_info[gd_count][3]
            str_value=decimal_to_quaternary_with_padding(value_info,5)
            for i in range(5):
                Robot2Move(i, int(str_value[i]), re_robot)
            flag=5
            continue
        #复位,读取下一个货物
        elif flag==5:
            for i in range(len(re_robot)):
                if re_robot[i] !=-1:
                    print("move", i, re_robot[i])
                    sys.stdout.flush()
                    re_robot[i] = -1
            gd_count+=1
            flag=0
            continue
        # logging.error("zhen:%d,id:%d", zhen, id)
        # for i in range(robot_num):
        #     print("move", i, random.randint(0, 3))
        #     sys.stdout.flush()
        print("OK")
        sys.stdout.flush()
