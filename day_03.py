import numpy

with open('day') as f: txt = f.read()

lines = txt.splitlines()

total = 0

# Parse and flag the elements
num_string = ''
adjacent = None
gears = {}
        
for row, line in enumerate(lines):
    for column, element in enumerate(line):
        
        # Check only if a number
        if element in '0123456789':
            num_string += element
            
            # Check the cardinal directions
            top_left = (row - 1 if row else row, column - 1 if column else column)
            bottom_right = (row + 2 if row < len(lines) - 1 else row, column + 2 if column < len(line) - 1 else column)
            
            for y in range(top_left[0], bottom_right[0]):
                for x in range(top_left[1], bottom_right[1]):
                    if lines[y][x] not in '0123456789.':
                        adjacent = (lines[y][x], x, y)
                        
        elif num_string:
            if adjacent:
                total += int(num_string)
                
                if adjacent[0] == '*':
                    
                    # This can really be done better :/
                    # Use the gear's position as a key and add the value to the list of values (or create a new list if none exists)
                    gears[f"x{adjacent[1]}y{adjacent[2]}"] = gears[f"x{adjacent[1]}y{adjacent[2]}"] + [int(num_string)] if gears.get(f"x{adjacent[1]}y{adjacent[2]}") else [int(num_string)]
                    
            num_string = ''
            adjacent = None

# Part 1
print(total)

# Part 2
print(sum([numpy.prod(list(gear)) if len(gear) == 2 else 0 for gear in list(gears.values())]))
