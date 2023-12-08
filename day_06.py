import re
import math

lines = open('day').read().splitlines()

times = re.findall("\d+", lines[0].split(":")[1])
records = re.findall("\d+", lines[1].split(":")[1])

def do_score(races):
    score = 1
    
    for race in races:
        time = int(race[0])
        record = int(race[1]) + 1
        
        # Quadratic magic
        limit_1 = math.ceil((time-math.sqrt((-time)**2 - (4 * record)))/2)
        limit_2 = time - limit_1
        
        versions  = (limit_2 - limit_1) + 1
        score *= versions
        
    return score

# Part 1
print(do_score(tuple(zip(times, records))))

# Part 2
print(do_score([(''.join(times), ''.join(records))]))
