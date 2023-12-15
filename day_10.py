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
current_direction = 0
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
        current_direction = direction
        current_coord = (start_coords[0] + offset_x, start_coords[1] + offset_y)
        break

# Step through the pipes until we reach 'S' again.
# Track the farthest point while we're at it.
steps = 1
current_pipe = map_grid[current_coord[1]][current_coord[0]]

left_turns = 0
right_turns = 0

path_coords = deque([current_coord])   # Track the coords that are part of our path for Part 2
path_directions = deque([current_direction])

while current_pipe != 'S':
    pipe_mask = pipe_bit_mask[current_pipe]
    
    # Check if we're turning and add to the counters.
    if (pipe_mask ^ 0b1010) and (pipe_mask ^ 0b0101):
        if left_normal(reverse(current_direction)) & (pipe_mask ^ current_direction):
            left_turns += 1
        else:
            right_turns += 1
    
    # Move us to the next pipe.
    # Do this by flipping the bit (turning off) the direction we came from.
    # Since the pipes only have 2 active bits (connections), that will leave us with the direction
    #   we need to go.
    current_direction = pipe_mask ^ current_direction
    move_coord = direction_bit_mask[current_direction]
    
    # Flip the direction, since that's now where we came from.
    current_direction = current_direction ^ 0b1010 if current_direction & 0b1010 else current_direction ^ 0b0101
    
    current_coord = (current_coord[0] + move_coord[0], current_coord[1] + move_coord[1])
    current_pipe = map_grid[current_coord[1]][current_coord[0]]
    path_coords.append(current_coord)
    path_directions.append(current_direction)
    
    steps += 1

# Part 1
print(steps//2)

########################################
# Part 2 (wtf)
checked_coords = deque()
confirmed_coords = set()
check_normal = left_normal if left_turns > right_turns else right_normal

# Helper functions
def scan_normals(coord, normal, checked):
    offset_x, offset_y = direction_bit_mask[normal]
    
    target_coord = (coord[0] + offset_x, coord[1] + offset_y)
    while (not target_coord in path_coords) and (not target_coord in checked_coords):
        checked_coords.append(target_coord)
        target_coord = (target_coord[0] + offset_x, target_coord[1] + offset_y)

# Start by replacing the 'S' position with a valid pipe
pipe_mask = reverse(path_directions[0]) ^ path_directions[-1]
pipe = [pipe for pipe, bit_mask in pipe_bit_mask.items() if bit_mask == pipe_mask][0]
map_grid[start_coords[1]] = map_grid[start_coords[1]].replace('S', pipe)

# Scan each entering normal and exiting normal for the path coords.
for coord, direction in list(zip(path_coords, path_directions)):
    enter_normal = check_normal(reverse(direction))
    exit_normal = check_normal(direction ^ pipe_bit_mask[map_grid[coord[1]][coord[0]]])
    
    scan_normals(coord, enter_normal, checked_coords)
    scan_normals(coord, exit_normal, checked_coords)

# Go through each checked coord, confirm them and check the neighboring coords.
target_inner_coord = None
while len(checked_coords):
    target_inner_coord = checked_coords.popleft()
    confirmed_coords.add(target_inner_coord)
    
    for (offset_x, offset_y) in direction_bit_mask.values():
        target_coord = (target_inner_coord[0] + offset_x, target_inner_coord[1] + offset_y)
        if (not target_coord in path_coords) and (not target_coord in checked_coords) and (not target_coord in confirmed_coords):
            checked_coords.append(target_coord)
    

print(len(confirmed_coords))
