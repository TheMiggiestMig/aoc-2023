from heapq import heappush, heappop
from collections import deque
import time

lines = open("test").read().strip().splitlines()

nodes = []


def heuristic(node_a, node_b):
    return (node_b[0] - node_a[0])**2 + (node_b[1] - node_a[1])**2

def cost(map_grid, node):
    return int(map_grid[node[1]][node[0]])

def a_star(map_grid, start_node, end_node):
    open_nodes = []     # Nodes to be investigated.
    heappush(open_nodes, (0, start_node))
    
    g_score = {start_node:0}    # Current best score to reach node from the start
    f_score = {start_node:heuristic(start_node, end_node)}  # Current best guess score to reach end from start via this node
    
    mapped_nodes = {}       # The path to each node via its parent. Also keeps track of the direction taken from the node.
    
    map_width = len(map_grid[0]) - 1
    map_height = len(map_grid) - 1
    
    counter = 0
    
    while open_nodes:
        current_node = heappop(open_nodes)[1]
        
        # If we reached the end, give us the path taken.
        if current_node == end_node:
            full_path = deque([(current_node, 0, cost(map_grid, current_node))])
            
            while current_node in mapped_nodes and current_node != start_node:
                current_node, direction, node_cost = mapped_nodes[current_node]
                full_path.appendleft((current_node, direction, node_cost))
                
            return full_path
        
        # Check all our neighboring squares
        for neighbor, direction in [
            ((0, -1), 0b1000),  # North
            ((1, 0), 0b0100),  # East
            ((0, 1), 0b0010),  # South
            ((-1, 0), 0b0001),  # West
            ]:
                
            neighbor_node = (current_node[0] + neighbor[0], current_node[1] + neighbor[1])
            
            # Make sure the neighbor is in the map_grid bounds.
            # Otherwise skip this one.
            if neighbor_node[0] < 0 or neighbor_node[0] > map_width or neighbor_node[1] < 0 or neighbor_node[1] > map_height:
                continue
            
            # Check if we've travelled 3 times in this direction already.
            # If we have, skip this one.
            parent_node, parent_node_direction = mapped_nodes.get(current_node) or 0, 0
            grandparent_node, grandparent_node_direction = mapped_nodes.get(parent_node) or 0, 0
            greatgrandparent_node, greatgrandparent_node_direction = mapped_nodes.get(grandparent_node) or 0, 0
            if parent_node_direction & grandparent_node_direction & greatgrandparent_node_direction & direction:
                continue
            
            local_cost = cost(map_grid, neighbor_node)
            local_g_score = g_score[current_node] + local_cost
            if not g_score.get(neighbor_node) or local_g_score < g_score[neighbor_node]:
                mapped_nodes[neighbor_node] = (current_node, direction, cost(map_grid, neighbor_node))
                g_score[neighbor_node] = local_g_score
                f_score[neighbor_node] = local_g_score + heuristic(neighbor_node, end_node)
                if neighbor_node not in open_nodes:
                    heappush(open_nodes, (f_score[neighbor_node], neighbor_node))
    
    return None

path = a_star(lines, (0,0), (len(lines[0]) - 1,len(lines) - 1))

map_grid = [[c for c in line] for line in lines]

directions = {
    0b1000: '^',
    0b0100: '>',
    0b0010: 'v',
    0b0001: '<'
}
for node, direction, cost in path:
    if direction:
        map_grid[node[1]][node[0]] = directions[direction]

map_grid = [''.join(line) for line in map_grid]

while True:
    print('\n\n\n\n\n\n\n\n')
    [print(line) for line in lines]
    time.sleep(0.5)
    print('\n\n\n\n\n\n\n\n')
    [print(line) for line in map_grid]
    time.sleep(0.5)
