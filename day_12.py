import math
from functools import lru_cache

lines = [line.strip() for line in open("day").read().splitlines()]

rows = []
for line in lines:
    arrangement, numbers = line.split(' ')
    numbers = tuple([int(number) for number in numbers.split(',')])
    rows.append((arrangement, numbers))


@lru_cache(maxsize=None)
def scan_line(arrangement, numbers):
    if not len(numbers):
        if '#' in arrangement:
            return 0
        else:
            return 1
    if arrangement[0] == '#': return 0
    
    number = numbers[0]
    next_numbers = tuple(numbers[1:])
    space = len(arrangement) - (sum(numbers) + len(next_numbers))
    
    valid = 0
    
    for sp in range(space):
        test_str = (sp + 1) * '.' + number*'#'
        
        test = all([a in [t,'?'] for a, t in zip(arrangement[:number + sp + 1], test_str)])
        if test:
            valid += scan_line(arrangement[number + sp + 1:], next_numbers)
    return valid

arrangement, numbers = rows[4]

# Part 1
print(sum([scan_line('.' + arrangement, numbers) for arrangement, numbers in rows]))

# Part 2
print(sum([scan_line('.' + '?'.join([arrangement] * 5), tuple(numbers * 5)) for arrangement, numbers in rows]))
