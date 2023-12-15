import re
from collections import deque

with open('day') as f: txt = f.read()

lines = txt.splitlines()

# Do the thing
def expand_universe(lines, scale=1):
    galaxies = deque()
    
    y_gap = 0
    x_gap = 0
    total_distance = 0
    
    # Find all the galaxies (and apply the y-expansion as you go).
    for y, line in enumerate(lines):
        found_galaxies = deque([(i.start(), y + y_gap) for i in re.finditer('#', line)])
        if len(found_galaxies):
            galaxies += found_galaxies
        else:
            y_gap += (scale - 1)
    
    galaxies = sorted(galaxies)
    
    # Apply the x-expansion to the galaxies
    previous_x = 0
    for galaxy_index, (galaxy_x, galaxy_y) in enumerate(galaxies):
        x_gap += (((galaxy_x - previous_x) or 1) - 1) * (scale - 1)
        previous_x = galaxy_x
        galaxies[galaxy_index] = (galaxy_x + x_gap, galaxy_y)
    
    # Iterate through each galaxy pair and sum the distances.
    for galaxy_index in range(len(galaxies) - 1):
        source_galaxy_x, source_galaxy_y = galaxies[galaxy_index]
        
        for (destination_galaxy_x, destination_galaxy_y) in galaxies[galaxy_index + 1:]:
            total_distance += abs(destination_galaxy_x - source_galaxy_x)
            total_distance += abs(destination_galaxy_y - source_galaxy_y)
            
    return total_distance


# Part 1
print(expand_universe(lines, 2))

# Part 2
print(expand_universe(lines, 1000000))
