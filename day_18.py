import numpy
from collections import deque
from heapq import heappush, heappop

lines = open('day').read().strip().splitlines()

direction_map = {
    'R': (1, 0),
    'D': (0, 1),
    'L': (-1, 0),
    'U': (0, -1)
}

# Generate all the points for the directions given
def generate_path(instructions):
    x, y = (0,0)
    points = deque()
    perimeter = 0
    
    for direction, length in [line.split(' ') for line in instructions]:
        length = int(length)
        delta_x, delta_y = direction_map[direction]
        
        x, y = x + (delta_x * length), y + (delta_y * length)
        
        perimeter += abs((delta_x * length))
        perimeter += abs((delta_y * length))
        
        points.append((x, y))
    return (points, perimeter)

# Math magic, Shoelace Formula to get area of the the shape.
def shoelace(points, perimeter):
    xy = numpy.array(points)
    xy = xy.reshape(-1, 2)

    x = xy[:,0]
    y = xy[:,1]

    S1 = numpy.sum(x * numpy.roll(y, -1))
    S2 = numpy.sum(y * numpy.roll(x, -1))

    return numpy.absolute(S1 - S2) // 2 + perimeter // 2 + 1

# Part 1
print(shoelace(*generate_path([' '.join(line.split(' ')[:-1])for line in lines])))

# Part 2
hex_encoded = ['0x' + line.split(' ')[-1][2:-1] for line in lines]
instructions = deque()

direction_keys = tuple(direction_map.keys())

for hex_code in hex_encoded:
    instructions.append(direction_keys[int('0x'+hex_code[-1], 16)] + ' ' + str(int(hex_code[:-1], 16)))

#[print(line) for line in instructions]
print(shoelace(*generate_path(instructions)))
