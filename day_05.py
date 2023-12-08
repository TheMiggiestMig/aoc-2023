from collections import deque

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
    
# Parse the input into mappings
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
    mappings[mapping_type][int(source)] = {'destination': int(dest), 'size': int(range_size)}

for key, value in mappings.items():
    mappings[key] = dict(sorted(value.items()))


# Map the seed ranges
# Note: This is a general solution made after Part 2 was revealed. Part 1's input will be interpreted differently to account for this.
def solve(seed_ranges):
    test_ranges = deque(seed_ranges)
    new_ranges = deque()
    source = categories[0]
        
    # Check each of the mappings.
    for destination in categories[1:]:
        mapping_type = f"{source}-to-{destination}"
        current_mapping = mappings[mapping_type]
        
        # Check each of the ranges in the mapping.
        while len(test_ranges):
            current_range = test_ranges.popleft()
            mapped = None  # Track if a mapping was found. If not, it passes through unmapped.
            
            
            for current_mapping_range_source_start in current_mapping:
                current_mapping_range = current_mapping[current_mapping_range_source_start]
                
                # Prepare the range and mapping bounds.
                mapping_source_left = current_mapping_range_source_start
                mapping_source_right = current_mapping_range_source_start + current_mapping_range['size'] - 1
                range_left = current_range['start']
                range_right = current_range['start'] + current_range['size'] - 1
                
                # If the range doesn't overlap, dismiss it.
                if range_left > mapping_source_right or range_right < mapping_source_left:
                    continue
                
                # If the range is completely within the mapping range, re-map it entirely.
                if range_left >= mapping_source_left and range_right <= mapping_source_right:
                    mapped = {'start': range_left - mapping_source_left + current_mapping_range['destination'],
                                            # Re-map the start of the range.
                                        'size':current_range['size']}
                                            # Keep the same size; no truncating required.
                    
                    break
                
                # At this point, there must be a complete or partial overlap. Map the overlapping parts,
                # and add the offcuts back to the test_ranges to check against the other mappings.
                overlap_left = 0
                overlap_right = 0
                if range_left < mapping_source_left:
                    overlap_left = mapping_source_left
                    overlap_right = min(mapping_source_right, range_right)
                else:
                    overlap_left = max(mapping_source_left, range_left)
                    overlap_right = mapping_source_right
                
                mapped = {'start': overlap_left - mapping_source_left + current_mapping_range['destination'],
                                            # Re-map the start of the range.
                                        'size':overlap_right - overlap_left + 1}
                
                # Recycle the offcuts (the left and/or right parts that don't overlap with the range)
                if overlap_left - range_left:
                    test_ranges.append({'start': range_left, 'size': overlap_left - range_left})
                if range_right - overlap_right:
                    test_ranges.append({'start': overlap_right + 1, 'size': range_right - overlap_right})
                    
                break
            
            # Append the new range (or pass through the current range if there were not overlaps found).
            new_ranges.append(mapped if mapped else current_range)
        
        # Repeat for the next category
        test_ranges = new_ranges
        new_ranges = deque()
        source = destination
    
    # The final category should "location", grab the starting point of the range with the lowest start.
    return min(test_ranges, key=lambda x: x['start'])['start']

# Part 1
# Using the general solution, we treat each seed as a range with a size of 1.
print(solve([{'start': seed, 'size': 1} for seed in seeds]))

# Part 2
print(solve([{'start': seeds[i], 'size': seeds[i + 1]} for i in range(0, len(seeds), 2)]))
