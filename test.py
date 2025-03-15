# def decimal_to_quaternary_with_padding(num, min_length):
#     """Convert a decimal number to its quaternary (base-4) representation as a string, with padding to ensure a minimum length."""
#     quaternary_str = ""
#     while num > 0:
#         remainder = num % 4
#         quaternary_str = str(remainder) + quaternary_str
#         num //= 4
# 
#     # Add leading zeros if the length is less than min_length
#     if len(quaternary_str) < min_length:
#         quaternary_str = quaternary_str.rjust(min_length, '0')
# 
#     return quaternary_str
# 
# 
# # Example usage with padding to ensure at least 6 digits
# decimal_to_quaternary_padded_example = decimal_to_quaternary_with_padding(1000, 6)
# print(decimal_to_quaternary_padded_example)

# def match_robots(previous_positions, current_positions):
#     if not previous_positions:
#         # 如果没有先前的位置，直接返回当前的位置
#         return current_positions
#
#     matched_positions = []
#     # 对每一个先前位置，找到当前位置中距离最近的
#     for pre in previous_positions:
#         matched_index, _ = min(enumerate(current_positions),
#                                key=lambda x: (x[1][0] - pre[0]) ** 2 + (x[1][1] - pre[1]) ** 2)
#         matched_positions.append(current_positions[matched_index])
#
#     return matched_positions
#
# pre=[(2, 2), (30, 29), (30, 68), (30, 129), (70, 29), (130, 29), (130, 168), (170, 29), (170, 68), (170, 129), (170, 168)]
#
# current_positions=[(2, 2), (30, 68), (30, 129), (30, 29), (70, 29), (130, 29), (130, 168), (170, 168), (170, 29), (170, 129), (170, 68), (170, 68)]
# new=match_robots(pre,current_positions)
# print(new)

line=[["1","a"],["1","a"],["1","a"],["1","a"]]
line2=[",".join(tmp) for tmp in line]
print(line2)
line3=" ".join(line2)
print(line3)