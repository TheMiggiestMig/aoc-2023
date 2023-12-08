import numpy

with open('day') as f: txt = f.read()

lines = txt.splitlines()
max_cubes = {'red':12, 'green':13, 'blue':14}   # For Part 1. Define the maximum number of cubes per color.

# Parse the games and calculate the power of each game (Part 2) while also determining if a game was possible or not (Part 1).
game_results = []

for game_index, game_line in enumerate(lines):
    game_cubes = {'red':0, 'green':0, 'blue':0}
    game_id = game_index + 1
    
    game = game_line.split(': ')[1]
    
    for game_round in game.split('; '):
        for pull in game_round.split(', '):
            num_cubes, cube = pull.split(' ')
            num_cubes = int(num_cubes)
            
            # Assign an ID of 0 if invalid (for calculating Part 1)
            if num_cubes > max_cubes[cube]:
                game_id = 0
            
            # Keep track of the highest of cubes for this game.
            if game_cubes[cube] < num_cubes:
                game_cubes[cube] = num_cubes
        
    game_results.append({'id': game_id, 'cubes': game_cubes})

# Part 1
# Sum of the valid game IDs (invalid game results are given an ID of 0).
print(sum([result['id'] for result in game_results]))

# Part 2
# Sum of the product of the number of cubes in each game.
print(sum([numpy.prod(list(result['cubes'].values())) for result in game_results]))
