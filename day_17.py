from heapq import heappush, heappop
from collections import deque
import time

lines = open("day").read().strip().splitlines()

map_grid = {(x,y):int(value) for y, line in enumerate(lines) for x, value in enumerate(line)}


def search(map_grid, start_node, end_node, min_steps, max_steps):
    open_nodes = []
    heappush(open_nodes, (0, *start_node, 0, 0, 0))
    
    visited_nodes = set()
    mapped_nodes = {}
    
    while open_nodes:
        node_heat, node_x, node_y, move_x, move_y, node_steps = heappop(open_nodes)
        current_state = (node_x, node_y, move_x, move_y)
        
        # We've reached the end.
        # Trace the path (since I like looking at things).
        if (node_x, node_y) == end_node:
            current_state = (node_x, node_y, move_x, move_y, node_steps)
            path = deque()
            [path.appendleft((node_x - (i * move_x), node_y - (i * move_y), move_x, move_y)) for i in range(node_steps)]
            while current_state[:2] != start_node:
                current_state = mapped_nodes[current_state][:-1]
                
                node_x, node_y, move_x, move_y, node_steps = current_state
                [path.appendleft((node_x - (i * move_x), node_y - (i * move_y), move_x, move_y)) for i in range(node_steps)]
            return path, node_heat
        
        if current_state in visited_nodes:
            continue
        
        visited_nodes.add(current_state)
        
        for delta_x, delta_y in {
            (0, -1),
            (1, 0),
            (0, 1),
            (-1, 0)} - {
                (move_x, move_y),
                (-move_x, -move_y)
            }:
            prev_x, prev_y, current_heat = node_x, node_y, node_heat
            old_state = (prev_x, prev_y, move_x, move_y)
            
            for steps in range(max_steps):
                new_x, new_y = prev_x + delta_x, prev_y + delta_y
                new_state = (new_x, new_y, delta_x, delta_y)
                
                if map_grid.get((new_x, new_y)):
                    current_heat += map_grid[(new_x, new_y)]
                    
                    if steps + 1 > min_steps - 1:
                        heappush(open_nodes, (current_heat, *new_state, steps + 1))
                        if not mapped_nodes.get((*new_state, steps + 1)) or mapped_nodes[(*new_state, steps + 1)][-1] > current_heat:
                            mapped_nodes[(*new_state, steps + 1)] = (*current_state, node_steps, current_heat)
                        
                else:
                    break
                
                prev_x, prev_y = new_x, new_y
                old_state = new_state
                
    return None

# Part 1
path, heat = search(map_grid, min(map_grid), max(map_grid), 1, 3)
print(heat)

# Part 2
path, heat = search(map_grid, min(map_grid), max(map_grid), 4, 10)
print(heat)

# Pretty stuff... not needed for the challenge, just my peace of mind.
def render(raw_data, path):
    direction = {
        (0, -1): '^',
        (1, 0): '>',
        (0, 1): 'v',
        (-1, 0): '<'
    }

    mapped_grid = [[c for c in line] for line in raw_data]
    for x, y, dx, dy in path:
        if (dx, dy) != (0, 0):
            mapped_grid[y][x] = direction[(dx, dy)]

    mapped_grid = [''.join(line) for line in mapped_grid]

    while True:
        print('\n'*12)
        [print(line) for line in raw_data]
        print('\n','Heat: ',heat)
        time.sleep(0.25)
        
        print('\n'*12)
        [print(mapped_line) for mapped_line in mapped_grid]
        print('\n','Heat: ',heat)
        time.sleep(0.25)
    
# render(lines, path)
