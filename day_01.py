import re

with open('day') as f: txt = f.read()

lines = txt.splitlines()

# Extract the two digit number from the string
def get_num(line, numbers):
    re_num = f"{'|'.join(numbers)}"
    
    re_start = re.findall(f"^.*?({re_num})", line)[0]
    re_start = str(numbers.index(re_start)) if re_start in numbers else re_start
    
    re_end = re.findall(f"^.*({re_num})(?!{re_num}).*?$", line)[0]
    re_end = str(numbers.index(re_end)) if re_end in numbers else re_end
    
    return (int(re_start + re_end))

# Part 1
print(sum([get_num(line, ['\d']) for line in lines]))

# Part 2
print(sum([get_num(line, ['\d','one','two','three','four','five','six','seven','eight','nine']) for line in lines]))
