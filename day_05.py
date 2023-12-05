with open('day') as f: txt = f.read()

lines = txt.splitlines()

map_chain = ['seed',
            'soil',
            'fertilizer',
            'water',
            'light',
            'temperature',
            'humidity',
            'location']
            
# Parse the seeds
seeds = list(map(lambda x: int(x), lines[0].split('seeds: ')[1].split(' ')))

# Parse the mappings
mappings = {}
mapped_seeds = {}
category = ''

for line in lines[1:]:
    
    # Ignore blank lines
    if not line:
        continue
    
    # If it doesn't start with a number then it's probably a category. Sort the previous category (if it exists), and start a new one
    if not line[0].isdigit():
        if category:
            sorted_category = {}
            for key, value in sorted(mappings[category].items()):
                sorted_category[key] = value
                
            mappings[category] = sorted_category
        
        # Start a new category
        category = line.split(' map:')[0]
        mappings[category] = {}
        continue
    
    # If we get this far, it's probably a mapping value
    dest, start, range_size = line.split(' ')
    mappings[category][int(start)] = {'dest':int(dest), 'range':int(range_size)}

def map_seed(seed):
    seed_map = {}
    
    source = map_chain[0]
    seed_map[source] = seed
    
    for dest in map_chain[1:]:
        category = f"{source}-to-{dest}"
        source_start = None
        
        print(f"Mapping {category} using {source} ({seed_map[source]})...")
        
        # Find the closest range
        for i, value in list(mappings[category].items()):
            if i > seed_map[source]:
                break
            source_start = (i, value)
        
        seed_map[dest] = seed_map[source]
        if source_start:
            print(f"\tClosest {category} source found ({source_start[0]})")
            source_start = source_start[0]
            
            # Check if the value falls out of range
            diff = seed_map[source] - source_start
            print(diff, mappings[category][source_start]['range'])
            if diff < mappings[category][source_start]['range']:
                seed_map[dest] = mappings[category][source_start]['dest'] + diff
        else:
            print(f"\t{category} source not found!")
            
        source = dest
        
    return seed_map

for i in range(len(seeds)):
    seeds[i] = map_seed(seeds[i])
    
[print(seed) for seed in list(sorted(seeds, key=lambda x: x['location']))]

