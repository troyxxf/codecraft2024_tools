import chardet

# 由于执行状态重置，重新导入chardet并检测文件编码
# 使用chardet来检测文件编码
with open("./rep.py", "rb") as f:
    raw_data = f.read(5000)  # 读取一部分文件用于编码检测，以免文件过大时读取时间过长
    result = chardet.detect(raw_data)


print(result["encoding"])