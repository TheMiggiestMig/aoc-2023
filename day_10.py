import math
from collections import deque

map_grid = [line.strip() for line in open("day").read().splitlines()]

# WARNING: I wrote this solution this way because I hate everyone (inclusive) after 4hrs sleep or less.

# The keys for the pipe directions
'''
| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this 
'''
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
moves = [
    (-1, 0, 0b0100),    # Move East
    (0, -1, 0b0010),    # Move South
    (1, 0, 0b0001),     # Move West
    (0, 1, 0b1000)      # Move North
    ]

for move in moves:
    map_grid_point = map_grid[start_coords[1] + move[1]][start_coords[0] + move[0]]
    
    # If it is a '.', we don't care.
    if map_grid_point == '.':
        continue
    
    pipe = pipe_bit_mask[map_grid_point]
    
    direction = move[2]
    
    # Check if the grid point we're looking at points back to 'S'.
    if pipe & direction:
        current_direction = direction
        current_coord = (start_coords[0] + move[0], start_coords[1] + move[1])
        break

# Step through the pipes until we reach 'S' again.
# Track the farthest point while we're at it.
steps = 1
current_pipe = map_grid[current_coord[1]][current_coord[0]]
farthest_point = (1, steps)

path_coords = deque()   # Track the coords that are part of our path for Part 2
path_coords.append(current_coord)

while current_pipe != 'S':
    pipe_mask = pipe_bit_mask[current_pipe]
    
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
    
    steps += 1
    
    # Now track how far we are from the 'S'. Use good ol' Manhattan Distance.
    distance = math.sqrt((abs(current_coord[0] - start_coords[0])**2) + (abs(current_coord[1] - start_coords[1])**2))
    if distance > farthest_point[0]:
        farthest_point = (distance, steps)

# Part 1
print(steps//2)


# Part 2 (wtf)
print(path_coords)
    
