lines = open("day").read().splitlines()


# Find the next number in sequence.
# To do this, work down the delta lists until one is found that is all 0 values.
# 'reverse' flag for if you want to find the previous number in the sequence.
def determine_next_in_sequence(sequence, reverse=False):
    sequence = list(map(lambda x: int(x), sequence.split(' ')))
    index = 0
    
    delta_lists = []
    delta_lists.append(sequence)
    
    not_all_zeros = 1
    count = 0
    
    # Discover the top order sequence (all zeros).
    while not_all_zeros:
        not_all_zeros = 0
        current_delta_list = delta_lists[-1]
        new_delta_list = []
        count += 1
        
        for i in range(0, len(current_delta_list) - 1):
            delta = current_delta_list[i + 1] - current_delta_list[i]
            not_all_zeros |= delta
            
            new_delta_list.append(delta)
        
        delta_lists.append(new_delta_list)
    
    # Use the top order sequence factor to determine the next (or previous if reverse=True) in sequence.
    if reverse:
        next_in_sequence = delta_lists[-1][0]
        for delta_list in delta_lists[::-1]:
            next_in_sequence = delta_list[0] - next_in_sequence
    else:
        next_in_sequence = sum([current_sequence[-1] for current_sequence in delta_lists])
    
    return next_in_sequence


# Part 1
print(sum([determine_next_in_sequence(line) for line in lines]))

# Part 2
print(sum([determine_next_in_sequence(line, reverse=True) for line in lines]))
