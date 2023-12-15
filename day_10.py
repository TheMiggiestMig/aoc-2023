import math
from collections import deque

map_grid = [line.strip() for line in open("day").read().splitlines()]

# WARNING: I wrote this solution this way because after 4hrs sleep or less, I hate everyone (inclusive).

# The keys for the pipe directions
#
#   NESW
# 0b1111
direction_to_bit = {
    'N': 0b1000,
    'E': 0b0100,
    'S': 0b0010,
    'W': 0b0001,
}

direction_bit_to_offset = {
    0b1000: (0, -1),    # North
    0b0100: (1, 0),     # East
    0b0010: (0, 1),     # South
    0b0001: (-1, 0)     # West
}

pipe_bit_mask = {
    '|': 0b1010,    # NS (also used to bit flip vertical directions)
    '-': 0b0101,    # EW (also used to bit flip horizonal directions)
    'L': 0b1100,    # NE
    'J': 0b1001,    # NW
    '7': 0b0011,    # SW
    'F': 0b0110,    # SE
}


# Useful helper function.
# Reverses the direction (E <-> W or N <-> S)
def reverse(direction_bit):
    return direction_bit ^ (pipe_bit_mask['|'] if direction_bit & pipe_bit_mask['|'] else pipe_bit_mask['-'])


################################################
# Find the starting position
start_coord_x, start_coord_y = (0,0)

for y, row in enumerate(map_grid):
    if row.find('S') + 1:
        start_coord_x, start_coord_y =  (row.index('S'), y)


###################################################
# Find (one of) the first joining coords and the direction to take for it.
enter_direction = 0
exit_direction = 0

current_coord_x, current_coord_y = (0, 0)

for direction_bit, (offset_x, offset_y) in direction_bit_to_offset.items():
    map_grid_point = map_grid[start_coord_y + offset_y][start_coord_x + offset_x]
    
    # If it is a '.', we don't care.
    if map_grid_point == '.':
        continue
    
    pipe = pipe_bit_mask[map_grid_point]
    enter_direction = reverse(direction_bit)
    
    # Check if the coord we're looking at points back to 'S'.
    if pipe & enter_direction:
        current_coord_x, current_coord_y = (start_coord_x + offset_x, start_coord_y + offset_y)
        break

start_direction = reverse(enter_direction)
end_direction = 0

######################################################
# Part 1
# Step through the pipes until we reach 'S' again.
# Track the farthest point while we're at it.
steps = 1
current_pipe = map_grid[current_coord_y][current_coord_x]

# Track the direction we're turning the most
# to determine if the loop is clockwise or not.
# turns > 0 = clockwise, turns < 0 = counter-clockwise.
turns = 0   

# Map out the connected pipes for part 2.
path_grid = {
    current_coord_x:{
        current_coord_y:(enter_direction, exit_direction)
    }
}

# Follow the pipes and map them until we come across the start 'S'.
while current_pipe != 'S':
    # Determine the exit direction.
    # Do this by flipping the bit (turning off) the direction we came from.
    # Since the pipes only have 2 active bits (connections),
    # that will leave us with the direction we need to go.
    pipe_mask = pipe_bit_mask[current_pipe]
    exit_direction = pipe_mask ^ enter_direction
    
    # Check if we're turning and add / subtract from the counter.
    if (pipe_mask ^ pipe_bit_mask['|']) and (pipe_mask ^ pipe_bit_mask['-']):
        left_normal = reverse(enter_direction) << 1 & 0xf or 1
        if left_normal & (pipe_mask ^ enter_direction):
            turns -= 1
        else:
            turns += 1
    
    # Store this info in our grid for part 2.
    if not path_grid.get(current_coord_y):
        path_grid[current_coord_y] = {}
    
    path_grid[current_coord_y][current_coord_x] = (reverse(enter_direction), exit_direction)
    
    # Move to the next (connected pipe).
    enter_direction = reverse(exit_direction)
    offset_x, offset_y = direction_bit_to_offset[exit_direction]
    
    current_coord_x, current_coord_y = (current_coord_x + offset_x, current_coord_y + offset_y)
    current_pipe = map_grid[current_coord_y][current_coord_x]
    
    end_direction = enter_direction
    steps += 1
    
print(steps//2) # The farthest part in the pipe loop is just half the number of pipes.


########################################
# Part 2 (wtf)
# Set the 'S' coord details since we now know how it starts and ends
path_grid[start_coord_y][start_coord_x] = (reverse(end_direction), start_direction)

# Scan across each line and check if we are inside the zone or out.
inner_count = 0
for y, line in path_grid.items():
    min_x = min(line.keys())
    max_x = max(line.keys())
    inner_flag = False  # Only count coords if we're inside the loop.
    
    # If we're going clockwise, moving North (0b1000) puts us inside the loop,
    # and Moving South puts us back out of it.
    # Counter-clockwise is the opposite.
    clockwise = direction_to_bit['N'] if turns > 0 else direction_to_bit['S']
    
    for x in range(min_x, max_x + 1):
        if line.get(x):
            direction = line[x][0] | line[x][1]
            if direction & clockwise:
                inner_flag = True
            elif direction & (clockwise ^ pipe_bit_mask['|']):
                inner_flag = False
        
        elif inner_flag:
            inner_count += 1

print(inner_count)
