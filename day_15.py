import re
lines = open("day").read().strip().splitlines()

def HASH(string):
    value = 0
    c_value = 0
    for c in string:
        c_value = ord(c)
        value += c_value
        value *= 17
        value %= 256
        
    return value
    

print(sum([HASH(word) for word in lines[0].split(',')]))

boxes = {}

for check in lines[0].split(','):
    label, instruction, lense = re.findall(r'(.*?)([=\-])(\d*)', check)[0]
    
    if instruction == '-':
        for box in boxes.values():
            if box.get(label):
                del box[label]
    else:
        box_number = HASH(label)
        if not boxes.get(box_number):
            boxes[box_number] = {}
        boxes[box_number][label] = int(lense)

value = 0
for box_number, box in boxes.items():
    for index, lense in enumerate(box.values()):
        value += (box_number + 1) * (index + 1) * lense

print(value)
