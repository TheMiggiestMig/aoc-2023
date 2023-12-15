import math
from collections import deque

map_grid = [line.strip() for line in open("day").read().splitlines()]

# WARNING: I wrote this solution this way because after 4hrs sleep or less, I hate everyone (inclusive).

# The keys for the pipe directions
#
#   NESW
# 0b1111

direction_bit_mask = {
    0b1000: (0, -1),    # North
    0b0100: (1, 0),     # East
    0b0010: (0, 1),     # South
    0b0001: (-1, 0)     # West
}

pipe_bit_mask = {
    '|': 0b1010,    # NS
    '-': 0b0101,    # EW
    'L': 0b1100,    # NE
    'J': 0b1001,    # NW
    '7': 0b0011,    # SW
    'F': 0b0110,    # SE
}


# Helper functions
def left_normal(direction):
    return direction << 1 & 0xf or 1

def right_normal(direction):
    return direction >> 1 or 0b1000

def reverse(direction):
    return direction ^ (0b1010 if direction & 0b1010 else 0b0101)

# Find the starting position
def find_start(map_grid):
    for y, row in enumerate(map_grid):
        for x, value in enumerate(row):
            if value == 'S':
                return (x, y)


start_coords = find_start(map_grid)

# Find one of the starting directions.
enter_direction = 0
exit_direction = 0
current_coord = (0, 0)

for direction_mask, (offset_x, offset_y) in direction_bit_mask.items():
    map_grid_point = map_grid[start_coords[1] + offset_y][start_coords[0] + offset_x]
    
    # If it is a '.', we don't care.
    if map_grid_point == '.':
        continue
    
    pipe = pipe_bit_mask[map_grid_point]
    
    direction = reverse(direction_mask)
    
    # Check if the grid point we're looking at points back to 'S'.
    if pipe & direction:
        enter_direction = direction
        current_coord = (start_coords[0] + offset_x, start_coords[1] + offset_y)
        break

# Step through the pipes until we reach 'S' again.
# Track the farthest point while we're at it.
steps = 1
current_pipe = map_grid[current_coord[1]][current_coord[0]]

left_turns = 0
right_turns = 0

path_coords = deque([current_coord])   # Track the coords that are part of our path for Part 2
path_directions = deque([enter_direction])
path_grid = {
    current_coord[0]:{
        current_coord[1]:(enter_direction, exit_direction)
    }
}

while current_pipe != 'S':
    pipe_mask = pipe_bit_mask[current_pipe]
    exit_direction = pipe_mask ^ enter_direction
    
    # Check if we're turning and add to the counters.
    if (pipe_mask ^ 0b1010) and (pipe_mask ^ 0b0101):
        if left_normal(reverse(enter_direction)) & (pipe_mask ^ enter_direction):
            left_turns += 1
        else:
            right_turns += 1
    
    # Move us to the next pipe.
    # Do this by flipping the bit (turning off) the direction we came from.
    # Since the pipes only have 2 active bits (connections), that will leave us with the direction
    #   we need to go.
    move_coord = direction_bit_mask[exit_direction]
    
    # Store this info in our grid for part 2.
    if not path_grid.get(current_coord[1]):
        path_grid[current_coord[1]] = {}
    
    path_grid[current_coord[1]][current_coord[0]] = (reverse(enter_direction), exit_direction)
    
    # Flip the direction, since that's now where we came from.
    enter_direction = exit_direction ^ 0b1010 if exit_direction & 0b1010 else exit_direction ^ 0b0101
    
    current_coord = (current_coord[0] + move_coord[0], current_coord[1] + move_coord[1])
    current_pipe = map_grid[current_coord[1]][current_coord[0]]
    path_coords.append(current_coord)
    path_directions.append(enter_direction)
    
    steps += 1

# Part 1
print(steps//2)

########################################
# Part 2 (wtf)
# Set the 'S' coord details since we now know where it starts and ends

path_grid[start_coords[1]][start_coords[0]] = (reverse(path_directions[-1]), reverse(path_directions[0]))

# Scan across each line and check if we are inside the zone or out.
inner_count = 0
for y, line in path_grid.items():
    min_x = min(line.keys())
    max_x = max(line.keys())
    inner_flag = False
    clockwise = 0b1000 if right_turns > left_turns else 0b0010
    
    for x in range(min_x, max_x + 1):
        if line.get(x):
            direction = line[x][0] | line[x][1]
            if direction & clockwise:
                inner_flag = True
            elif direction & (clockwise ^ 0b1010):
                inner_flag = False
        
        if x not in line.keys() and inner_flag:
            inner_count += 1

print(inner_count)
