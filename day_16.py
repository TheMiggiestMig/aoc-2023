from collections import deque

lines = [line.strip() for line in open("day").read().splitlines()]

#   NESW
# 0b1111
direction_bit_to_coord = {
    0b1000: (0, -1),
    0b0100: (1, 0),
    0b0010: (0, 1),
    0b0001: (-1, 0)
}


def fire_beam(beam):
    beams = deque([beam])
    energized_point = {}
    
    while len(beams):
        x, y, direction = beams.pop()
        
        while True:
            # Check if we're hitting a boundary
            if x < 0 or y < 0 or x >= len(lines[0]) or y >= len(lines):
                break
            
            # Energize this grid point.
            if energized_point.get((x, y)):
                if energized_point[(x, y)] & direction:
                    break
                else:
                    energized_point[(x, y)] |= direction
            else:
                energized_point[(x, y)] = direction
            
            # Get ready to move the beam.
            delta_x, delta_y = direction_bit_to_coord[direction]
            
            # Check if we're on a special square.
            grid_point = lines[y][x]
            if grid_point == "/":
                direction = direction ^ (0b1100 if direction & 0b1100 else 0b0011)
                delta_x, delta_y = direction_bit_to_coord[direction]
            elif grid_point == "\\":
                direction = direction ^ (0b0110 if direction & 0b0110 else 0b1001)
                delta_x, delta_y = direction_bit_to_coord[direction]
            elif grid_point == "|":
                if direction & 0b0101:
                    north = direction_bit_to_coord[0b1000][1]
                    south = direction_bit_to_coord[0b0010][1]
                    beams.appendleft((x, y + north, 0b1000))
                    beams.appendleft((x, y + south, 0b0010))
                    break
            elif grid_point == "-":
                if direction & 0b1010:
                    east = direction_bit_to_coord[0b0100][0]
                    west = direction_bit_to_coord[0b0001][0]
                    beams.appendleft((x + east, y, 0b0100))
                    beams.appendleft((x + west, y, 0b0001))
                    break
            
            x, y = (x + delta_x, y + delta_y)
            
    return len(energized_point)
# Part 1
print(fire_beam((0,0, 0b0100)))

# Part 2
max_points = 0
for x in range(len(lines[0])):
    max_points = max(max_points, fire_beam((x, 0, 0b0010)), fire_beam((x, len(lines) - 1, 0b1000)))

for y in range(len(lines)):
    max_points = max(max_points, fire_beam((0, y, 0b0100)), fire_beam((len(lines[0]) - 1, y, 0b0001)))

print(max_points)
