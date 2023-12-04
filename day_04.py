import numpy

with open('day') as f: txt = f.read()

lines = txt.splitlines()
total = 0

for line in lines:
    nums = line.split(': ')[1].split(' | ')
    win_nums = nums[0].split(' ')
    scratch_nums = nums[1].split(' ')
    wins = 0
    
    for win_num in win_nums:
        if win_num and win_num in scratch_nums:
            wins += 1
    
    if wins:
        total += pow(2, wins - 1)

print(total)
