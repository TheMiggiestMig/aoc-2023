import numpy

lines = open('day').read().splitlines()

instructions = lines[0]
desert_map = {}

# Process the map into a dict.
for line in lines[2:]:
    key, lr = line.split(' = ')
    l,r = lr[1:-1].split(', ')
    desert_map[key] = {'L':l, 'R':r}


# Part 1
current_position = 'AAA'
target_position = 'ZZZ'

current_instruction = 0
steps = 0

while current_position != target_position:
    # Move according to our current instruction.
    current_position = desert_map[current_position][instructions[current_instruction]]
    
    steps += 1
    current_instruction = (current_instruction + 1) % len(instructions)

print(steps)

# Part 2
# Find how many steps it takes for EACH starting point to reach a valid destination.
current_positions = [key for key in desert_map.keys() if key[-1] == 'A']
steps_taken = []

for key in current_positions:
    current_position = key
    current_instruction = 0
    steps = 0
    
    while current_position[-1] != 'Z':
        current_position = desert_map[current_position][instructions[current_instruction]]
    
        steps += 1
        current_instruction = (current_instruction + 1) % len(instructions)
    steps_taken.append(steps)

# LCM. Honestly, I took a wild stab at it after looking at patterns, following a hunch.
# For truly random (but solvable) inputs, they are highly unlikely to end up in perfectly nice loops,
# especially the first pass... but my hunch paid off for this one :)
print(numpy.lcm.reduce(steps_taken))
