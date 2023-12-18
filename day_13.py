lines = [line.strip() for line in open("day").read().splitlines()]

segments = []
segment = []

for line in lines:
    if not line:
        segments.append(segment)
        segment = []
        continue
    segment.append(line)
segments.append(segment)


def search_for_split(segment, smudges=0):
    errors = 0
    path_width = len(segment[0])
    for mirror_x in range(1, path_width):
        for distance in range(mirror_x):
            if mirror_x + distance > path_width - 1:
                    break
                
            for line in segment:
                left = line[mirror_x - distance - 1]
                right = line[mirror_x + distance]
                
                if left != right:
                    errors += 1
                    
                if errors > smudges:
                    break
            else:
                continue
            break
        
        if errors == smudges:
            return mirror_x
        errors = 0
    else:
        return 0


for smudges in [0,1]:
    values = []
    for index, segment in enumerate(segments):
        value = 0
        value += search_for_split(segment, smudges)
        
        if value == 0:
            value += 100 * search_for_split(list(map(lambda l: ''.join(l), zip(*segment))), smudges)
            
        values.append(value)
    print(sum(values))
