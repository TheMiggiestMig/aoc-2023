import re

with open('day') as f: txt = f.read()

input_lines = txt.splitlines()

# General solution for Part 1 and Part 2
def solve(lines, numbers):
    re_num = f"{'|'.join(numbers)}"     # convert an array of strings into a regular expression capture group.
    total = 0
    
    # Extract the two digit number from each line.
    for line in lines:
        
        # Search from the start of the string.
        re_start = re.findall(f"^.*?({re_num})", line)
        re_start = '' if not len(re_start) else str(numbers.index(re_start[0])) if re_start[0] in numbers else re_start[0]
        #                                                      ^ No need to deal with adjusting 0-indexed array, see below
        
        # Search from the end of the string.
        re_end = re.findall(f"^.*({re_num})", line)
        re_end = '0' if not len(re_end) else str(numbers.index(re_end[0])) if re_end[0] and re_end[0] in numbers else re_end[0]
        #                                                      ^ No need to deal with adjusting 0-indexed array, see below
        
        total += int(re_start + re_end)
    
    return total


# Part 1
print(solve(input_lines, ['\d']))

# Part 2
# Dirty trick in order to not deal with 0-indexed array: use the '\d' to offset it by 1 :p
print(solve(input_lines, ['\d','one','two','three','four','five','six','seven','eight','nine']))
