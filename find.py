# 重新执行之前的计算因为执行环境重置了
from itertools import permutations

# # 港口的运输时间
# port_travel_times = {
#     0: 800,
#     1: 1022,
#     2: 931,
#     3: 988,
#     4: 1117,
#     5: 1140,
#     6: 930,
#     7: 1020,
#     8: 1091,
#     9: 991,
# }# 港口的运输时间
port_travel_times = {
    0: 858,
    1: 1080,
    2: 989,
    3: 1046,
    4: 1175,
    5: 1198,
    6: 988,
    7: 1078,
    8: 1149,
    9: 1049,
}

# 转运时间
trans_time = 500

# 计算所有可能的配对及其总运输时间
pair_travel_times = {}
results=[]
for i1 in range(10):
    for i2 in range(10):
        if i2!=i1:
            for i3 in range(10):
                if i3!=i2 and i3!=i1:
                    for i4 in range(10):
                        if i4!=i1 and i4!=i2 and i4!=i3:
                            for i5 in range(10):
                                if i5!=i4 and i5!=i3 and i5!=i2 and i5!=i1:
                                    for i6 in range(10):
                                        if i6!=i5 and i6!=i4 and i6!=i3 and i6!=i2 and i6!=i1:
                                            for i7 in range(10):
                                                if i7!=i6 and  i7!= i5 and i7 != i4 and i7 != i3 and i7 != i2 and i7 != i1:
                                                    for i8 in range(10):
                                                        if i8!=i7 and i8!=i6 and  i8!= i5 and i8 != i4 and i8 != i3 and i8 != i2 and i8 != i1:
                                                            for i9 in range(10):
                                                                if i9!=i8 and i9!= i7 and i9 != i6 and i9 != i5 and i9 != i4 and i9 != i3 and i9 != i2 and i9 != i1:
                                                                    for i10 in range(10):
                                                                        if i10!=i9 and i10!= i8 and i10 != i7 and i10 != i6 and i10 != i5 and i10 != i4 and i10 != i3 and i10 != i2 and i10 != i1:
                                                                            total_time1=port_travel_times[i1] + trans_time + port_travel_times[i2]

                                                                            total_time2 = port_travel_times[
                                                                                              i3] + trans_time + \
                                                                                          port_travel_times[i4]
                                                                            total_time3 = port_travel_times[
                                                                                              i5] + trans_time + \
                                                                                          port_travel_times[i6]
                                                                            total_time4 = port_travel_times[
                                                                                              i7] + trans_time + \
                                                                                          port_travel_times[i8]
                                                                            total_time5 = port_travel_times[
                                                                                              i9] + trans_time + \
                                                                                          port_travel_times[i10]
                                                                            total_time_list=[total_time1,total_time2,total_time3,total_time4,total_time5]
                                                                            result_tmp=[]
                                                                            for id in range(len(total_time_list)):
                                                                                total_time=total_time_list[id]
                                                                                trips = 15000 // total_time  # 往返次数
                                                                                unused_time = 15000 - (
                                                                                            trips * total_time)  # 未运输的时间
                                                                                if id==0:
                                                                                    result_tmp.append((i1,i2,trips,unused_time))
                                                                                elif id==1:
                                                                                    result_tmp.append(
                                                                                        (i3, i4, trips, unused_time))
                                                                                elif id==2:
                                                                                    result_tmp.append(
                                                                                        (i5, i6, trips, unused_time))
                                                                                elif id==3:
                                                                                    result_tmp.append(
                                                                                        (i7, i8, trips, unused_time))
                                                                                elif id==4:
                                                                                    result_tmp.append(
                                                                                        (i9, i10, trips, unused_time))
                                                                            # if result_tmp not in results:
                                                                            results.append(result_tmp)

print(results)

sorted_results = [list(t) for t in {tuple(item) for item in results}]


sorted_results = sorted(sorted_results, key=lambda x: sum(item[3] for item in x))


# 输出最小的十个result
print("最小的十个result：")
for i, result in enumerate(sorted_results[:10], 1):
    print(f"{i}. {result}   {sum([i[3] for i in result])}")


# min_sum = float('inf')
# min_result = None
#
# # 遍历每个result，计算第四个元素的总和
# for result in results:
#     total_sum = sum(item[3] for item in result)
#     # 更新最小总和和对应的result
#     if total_sum < min_sum:
#         min_sum = total_sum
#         min_result = result
#
# print("所有第四个元素相加结果最小的result：", min_result)

# # 计算每个配对在15000时间内能完成的最大往返次数
# max_trips_per_pair = {pair: 15000 // (time + trans_time) for pair, time in pair_travel_times.items()}
#
# # 对配对按能完成的最大往返次数进行排序
# sorted_pairs_by_trips = sorted(max_trips_per_pair.items(), key=lambda x: x[1], reverse=True)
#
# # 选择能完成最多往返次数的前5个配对
# optimal_pairs_by_trips = sorted_pairs_by_trips[:5]

