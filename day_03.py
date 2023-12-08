import numpy

with open('day') as f: txt = f.read()
lines = txt.splitlines()

total = 0   # For Part 1
part_number = ''
adjacent_symbols = {}
gears = {}
        
for row, line in enumerate(lines):
    for column, element in enumerate(line):
        
        # We'll extract the numbers on each line, and base everything from them.
        if element.isdigit():
            part_number += element
            
            # Check the neighboring squares for symbols, keeping within the bounds.
            bounds = {
                'top': row - 1 if row else row,
                'left': column - 1 if column else column,
                'bottom': row + 2 if row < len(lines) - 1 else row,
                'right':column + 2 if column < len(line) - 1 else column
            }
            
            for y in range(bounds['top'], bounds['bottom']):
                for x in range(bounds['left'], bounds['right']):
                    
                    if lines[y][x] not in '0123456789.':    # Not a number or '.', so a symbol.
                        adjacent_symbols[(x, y)] = lines[y][x]
        
        # If it's not a number and we have previously detected numbers, then we've reached the end of the number.
        # Check if it's a part number by seeing if it was adjacent to any symbols.
        elif part_number:
            if len(adjacent_symbols):
                
                # Add the part number to the total (Part 1)
                total += int(part_number)
                
                for symbol_coords in adjacent_symbols:
                    symbol = adjacent_symbols[symbol_coords]
                    if symbol == '*':
                        
                        # Use the gear's position as a key and add the value to the list of values (or create a new list if none exists)
                        if not gears.get(symbol_coords):
                            gears[symbol_coords] = []
                            
                        gears[symbol_coords] += [int(part_number)]
                    
            part_number = ''
            adjacent_symbols = {}

# Part 1
print(total)

# Part 2
print(sum([numpy.prod(list(gear)) if len(gear) == 2 else 0 for gear in list(gears.values())]))
