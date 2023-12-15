import re
from collections import deque
from itertools import combinations

# Used [this](https://towardsdatascience.com/solving-nonograms-with-120-lines-of-code-a7c6e0f627e4) as a reference.

with open('day') as f: txt = f.read()

lines = txt.splitlines()

def number_map_to_arrangement(numbers, positions, length):
    cursor_position = 0
    pairings = list(zip(positions, numbers))
    arrangement = ''
    
    for position, value in pairings:
        arrangement += f"{'.'*(position - cursor_position)}{'#' * value}"
        cursor_position = position
    
    arrangement = arrangement.ljust(length, '.')
    
    return arrangement

total_combinations = 0

for line in lines:
    arrangement, numbers = line.split(' ')
    numbers = [int(number) for number in numbers.split(',')]
    total_space = len(arrangement)
    required_space = sum(numbers) + len(numbers) - 1
    extra_space = len(arrangement) - required_space
    
    # determine all combinations of possible placements
    possibilities = list(combinations(range(len(numbers) + extra_space), len(numbers)))
    for test_case in possibilities:
        test_arrangement = number_map_to_arrangement(numbers, test_case, total_space)
        valid = 1
        
        for index, char in enumerate(arrangement):
            if char == '?': continue
            if char != test_arrangement[index]:
                valid = 0
                break
        total_combinations += valid

# Part 1
print(total_combinations)

# Part 2 (This isn't gonna work for part 2)
