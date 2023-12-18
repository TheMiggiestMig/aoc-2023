from functools import lru_cache

lines = open("day").read().strip().splitlines()

@lru_cache(maxsize=None)
def tilt_up(input_lines):
    lines = [[c for c in line] for line in list(input_lines)]
    value = 0
    
    for line_index, line in enumerate(lines):
        for rock_index, rock in enumerate(line):
            if rock != 'O':
                continue
            current_index = line_index
            while True:
                if current_index <= 0 or lines[current_index - 1][rock_index] in "O#":
                    break
                
                lines[current_index][rock_index] = '.'
                lines[current_index - 1][rock_index] = 'O'
                current_index -= 1
    return tuple([''.join(line) for line in lines])


@lru_cache(maxsize=None)
def rotate(input_lines):
    return tuple([''.join(line) for line in zip(*input_lines[::-1])])


@lru_cache(maxsize=None)
def spin(input_lines):
    lines = input_lines
    
    for turn in range(4):
        lines = rotate(tilt_up(lines))
    
    return lines


def score(input_lines):
    value = 0
    value_matrix = {}
    for index, line in enumerate(input_lines):
        value_matrix[len(input_lines) - index] = line.count('O')
        value += line.count('O') * (len(input_lines) - index)
    
    return value
    
print(score(tilt_up(tuple(lines))))


value = 0
lines = tuple(lines)

results = {}
for index in range(1000000000):
    lines = spin(lines)
    if results.get(lines):
        break
    results[lines] = index

modulo_spins = (1000000000 - results[lines]) % (index - results[lines]) - 1

for index in range(modulo_spins):
    lines = spin(lines)

print(score(lines))
