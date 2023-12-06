with open('day') as f: txt = f.read()

lines = txt.splitlines()

seeds = list(map(lambda x: int(x), lines[0].split('seeds: ')[1].split(' ')))
categories = [
    'seed',
    'soil',
    'fertilizer',
    'water',
    'light',
    'temperature',
    'humidity',
    'location'
    ]
    
# Parse the mappings
mappings = {}

mapping = {}
mapping_type = ''
for line in lines[1:]:
    
    # Ignore blank lines
    if not line: continue
    
    # If it doesn't start with a number, it's probably a new category
    if not line[0].isdigit():
        mapping_type = line.split(' map:')[0]
        mappings[mapping_type] = {}
        continue
    
    # Add the items
    dest, source, range_size = line.split(' ')
    mappings[mapping_type][int(source)] = {'dest': int(dest), 'range': int(range_size)}

for key, value in mappings.items():
    mappings[key] = dict(sorted(value.items()))

# Parse the seeds
def map_seed(seed):
    mapped_seed = {}
    source = categories[0]
    mapped_seed[source] = seed
    
    # Follow the mappings
    for dest in categories[1:]:
        mapping_type = f"{source}-to-{dest}"
        
        source_range_start = None
        for source_start, item in mappings[mapping_type].items():
            if source_start > mapped_seed[source]:
                break
            source_range_start = (source_start, item)
        
        mapped_seed[dest] = mapped_seed[source]
        
        if source_range_start:
            diff = mapped_seed[source] - source_range_start[0]
            if diff < source_range_start[1]['range']:
                mapped_seed[dest] = source_range_start[1]['dest'] + diff
                
        source = dest
        
    return mapped_seed

seeds = list(map(lambda x: map_seed(x), seeds))

# Part 1
print(list(sorted(seeds, key=lambda x: x['location']))[0]['location'])
