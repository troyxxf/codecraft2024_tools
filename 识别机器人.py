from PIL import Image
import time

def find_robots(image, black_threshold, min_pixels_per_robot):
    # 转换图像到灰度
    gray_image = image.convert('L')

    # 获取图像尺寸
    width, height = gray_image.size


    # 用于存储机器人位置的列表
    robots_positions = []

    # 已经检查过的像素
    checked_pixels = set()

    # 扫描每个像素
    for x in range(width):
        for y in range(height):
            if (x, y) in checked_pixels or gray_image.getpixel((x, y)) >= black_threshold:
                continue

            stack = [(x, y)]
            pixel_block = []

            while stack:
                px, py = stack.pop()
                if (px, py) in checked_pixels:
                    continue

                checked_pixels.add((px, py))
                pixel_value = gray_image.getpixel((px, py))
                if pixel_value < black_threshold:
                    pixel_block.append((px, py))
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if 0 <= px + dx < width and 0 <= py + dy < height:
                                stack.append((px + dx, py + dy))

            if len(pixel_block) >= min_pixels_per_robot:
                avg_x = sum(px for px, py in pixel_block) / len(pixel_block)
                avg_y = sum(py for px, py in pixel_block) / len(pixel_block)
                robots_positions.append((avg_x, avg_y))

    return robots_positions

def scale_positions(positions, original_size, target_size):
    scale_x = target_size[0] / original_size[0]
    scale_y = target_size[1] / original_size[1]
    return [(int(x * scale_x), int(y * scale_y)) for x, y in positions]

def sort_positions(positions):
    """ 根据从上到下，从左到右的顺序对位置进行排序 """
    # 首先按照y坐标排序，然后在y坐标相同的情况下按照x坐标排序
    return sorted(positions, key=lambda pos: (pos[1], pos[0]))

def match_robots(previous_positions, current_positions):
    if not previous_positions:
        # 如果没有先前的位置，直接返回当前的位置

        return sort_positions(current_positions)

    matched_positions = []
    # 对每一个先前位置，找到当前位置中距离最近的
    for pre in previous_positions:
        matched_index, _ = min(enumerate(current_positions),
                               key=lambda x: (x[1][0] - pre[0]) ** 2 + (x[1][1] - pre[1]) ** 2)
        matched_positions.append(current_positions[matched_index])

    return matched_positions

# def process_images(image_paths, crop_rectangle, black_threshold, min_pixels_per_robot, original_size, target_size):
#     for image_path in image_paths:
#         image = Image.open(image_path)
#         # width, height = image.size
#         # print(width,height)
#
#         # 裁剪图像
#         cropped_image = image.crop(crop_rectangle)
#         cropped_image.show()
#
#         # 找到机器人并调整坐标
#         robots_positions = find_robots(cropped_image, black_threshold, min_pixels_per_robot)
#         scaled_positions = scale_positions(robots_positions, original_size, target_size)
#
#         print(f"Image: {image_path}")
#         for position in scaled_positions:
#             print(position)


def process_images_and_detect_movement(image_paths, crop_rectangle, black_threshold, min_pixels_per_robot,
                                       original_size, target_size):
    previous_positions = None
    for image_path in image_paths:
        image = Image.open(image_path)
        cropped_image = image.crop(crop_rectangle)

        robots_positions = find_robots(cropped_image, black_threshold, min_pixels_per_robot)
        scaled_positions = scale_positions(robots_positions, original_size, target_size)
        scaled_positions = match_robots(previous_positions, scaled_positions)
        print(scaled_positions)

        if previous_positions is not None:
            # print(previous_positions)
            # print(scaled_positions)
            for i, (prev_pos, curr_pos) in enumerate(zip(previous_positions, scaled_positions)):
                dx = curr_pos[0] - prev_pos[0]
                dy = curr_pos[1] - prev_pos[1]

                if abs(dx) > 0 or abs(dy) > 0:
                    direction = ''
                    if dy < 0 :
                        direction += 'Up'
                    elif dy > 0:
                        direction += 'Down'
                    if dx < 0:
                        direction += 'Left'
                    elif dx > 0:
                        direction += 'Right'

                    if direction == '':
                        direction = 'Stationary'

                    print(f"Robot {i + 1} moved {direction} in {image_path}")
        print("__________________")
        previous_positions = scaled_positions

def generate_image_paths(start, end, base_path="./pic/output_frame_{}.png"):
    paths = [base_path.format(i) for i in range(start, end + 1)]
    return paths

# 参数设置
image_paths = generate_image_paths(17, 25)  # 这里添加你要处理的图像路径
crop_rectangle = (0, 0, 799, 799)  # 裁剪参数
black_threshold = 50
min_pixels_per_robot = 5
original_size = (799, 799)  # 裁剪后图像的大小，这里稍微调整以符合你的实际情况
target_size = (200, 200)  # 目标图像的大小

# 处理图像
# process_images(image_paths, crop_rectangle, black_threshold, min_pixels_per_robot, original_size, target_size)
start=time.time()
process_images_and_detect_movement(image_paths, crop_rectangle, black_threshold, min_pixels_per_robot, original_size, target_size)
end=time.time()
print("TIme",end-start)
