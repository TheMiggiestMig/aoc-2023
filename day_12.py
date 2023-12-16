import math
from functools import lru_cache

lines = [line.strip() for line in open("day").read().splitlines()]

rows = []
for line in lines:
    arrangement, numbers = line.split(' ')
    rows.append((arrangement, numbers))


@lru_cache(maxsize=None)
def scan_line(arrangement, numbers):
    if not len(numbers):
        if arrangement.find('#')+1:
            return 0
        else:
            return 1
    if arrangement[0] == '#': return 0
    numbers = list([int(number) for number in numbers.split(',')])
    number = numbers[0]
    next_numbers = numbers[1:]
    space = len(arrangement) - (sum(numbers) + len(next_numbers))
    
    valid = 0
    
    for sp in range(space):
        test_str = (sp+1)*'.'+number*'#'
        
        test = all([a in [t,'?'] for a, t in zip(arrangement[:number+sp+1], test_str)])
        if test:
            valid += scan_line(arrangement[number+sp+1:], ','.join([str(num) for num in next_numbers]))
    return valid

arrangement, numbers = rows[4]


print(sum([scan_line('.'+arrangement, numbers) for arrangement, numbers in rows]))

print(sum([scan_line('.'+'?'.join([arrangement]*5), ','.join([numbers]*5)) for arrangement, numbers in rows]))