import re

with open('day') as f: txt = f.read()

input_lines = txt.splitlines()

# Extract the two digit number from the string
def get_num(lines, numbers):
    re_num = f"{'|'.join(numbers)}"
    total = 0
    
    for line in lines:
        re_start = re.findall(f"^.*?({re_num})", line)
        re_start = '' if not len(re_start) else str(numbers.index(re_start[0])) if re_start[0] in numbers else re_start[0]
        
        re_end = re.findall(f"^.*({re_num})", line)
        re_end = '0' if not len(re_end) else str(numbers.index(re_end[0])) if re_end[0] and re_end[0] in numbers else re_end[0]
        
        total += int(re_start + re_end)
    
    return (total)

# Part 1
print(get_num(input_lines, ['\d']))

# Part 2
print(get_num(input_lines, ['\d','one','two','three','four','five','six','seven','eight','nine']))
