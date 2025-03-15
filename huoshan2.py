import itertools
import matplotlib.pyplot as plt


# 扩散函数，模拟扩散
def spread_lava(map_data, start, moves):
    queue = [start]
    visited = set([start])
    for _ in range(moves):
        next_queue = []
        for x, y in queue:
            for dx, dy in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(map_data) and 0 <= ny < len(map_data[0]) and (nx, ny) not in visited and map_data[nx][ny] in ['.', 'B']:
                    visited.add((nx, ny))
                    next_queue.append((nx, ny))
        queue = next_queue
    return visited


def find_best_combinations_for_lava_moves(map_data, berths,  move_min, move_max, step = 5):
    result = {}
    for moves in range(move_min, move_max, step):
        current_best_combination = None
        current_best_coverage = 0
        for combination in itertools.combinations(berths, 5):  # 直接在berths上进行组合
            covered = set()
            for volcano in combination:
                covered |= spread_lava(map_data, volcano, moves)
            coverage = len(covered)
            if coverage > current_best_coverage:
                current_best_coverage = coverage
                current_best_combination = combination
        print("moves:", moves, " current_best_combination:", current_best_combination, "current_best_coverage:", current_best_coverage)
        if current_best_combination in result:
            result[current_best_combination] += 1
        else:
            result[current_best_combination] = 1

        # 创建绘图数据
        plot_data = [[0 for _ in range(len(map_data[0]))] for _ in range(len(map_data))]
        covered = set()
        for volcano in current_best_combination:

            covered |= spread_lava(map_data, volcano, moves)
        for x, y in covered:
            plot_data[x][y] = 1  # 标记岩浆覆盖区域
        for x, y in berths:
            plot_data[x][y] = 2  # 标记火山位置
        # 绘制图像
        plt.figure(figsize=(10, 10))
        plt.imshow(plot_data, cmap='hot')
        plt.colorbar(ticks=[0, 1, 2], label='Type')
        plt.title(f'Lava Moves: {moves}')
        plt.show()
    return result

if __name__ == '__main__':
    moves_list = [50, 60, 70, 80, 90, 100, 110]
    # 从文件中读取地图数据
    with open('mapmap2.txt', 'r') as file:
        map_data = [list(line.strip()) for line in file.readlines()]

    # 定位所有火山的中心位置
    berths = []
    berthId = {}
    id = 0
    for i, row in enumerate(map_data):
        for j, cell in enumerate(row):
            if cell == 'B' and map_data[i][j - 1] != 'B' and map_data[i - 1][j] != 'B':
                berths.append(((i + 2, j + 2)))
                berthId[(i + 2, j + 2)] = id
                id += 1
    move_min = 60
    move_max = 101
    step=5
    result = find_best_combinations_for_lava_moves(map_data, berths, move_min, move_max,)
    sorted_result = sorted(result.items(), key=lambda item: item[1], reverse=True)
    finnal_berthId = []
    for res in sorted_result:
        current_berthId = []
        for id in res[0]:
            current_berthId.append(berthId[id])
        finnal_berthId.append((current_berthId, res[1]))
    print(finnal_berthId)

