
with open('repmap2.txt', 'r') as file:
    lines = [line[1:] for line in file]


with open('mapmap2.txt', 'w') as file:
    for line in lines:
        file.write(line)
